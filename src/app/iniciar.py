"""Ejecutar ambos servicios en el equipo local y cerrar los procesos propios al salir."""
import subprocess
import sys
import time
import webbrowser

import requests

from src import config


def responde(url):
    try:
        return requests.get(url, timeout=.5).ok
    except requests.RequestException:
        return False


def iniciar(modulo, argumentos):
    return subprocess.Popen([sys.executable, "-m", modulo, *argumentos], cwd=config.RAIZ)


def main():
    ui = "http://127.0.0.1:8501"
    procesos = []
    try:
        if not responde(config.API_LOCAL + "/salud"):
            procesos.append(iniciar("uvicorn", ["src.api.main:app", "--host","127.0.0.1","--port","8000"]))
            for _ in range(100):
                if responde(config.API_LOCAL + "/salud") or procesos[-1].poll() is not None:
                    break
                time.sleep(.2)
        if not responde(ui + "/_stcore/health"):
            interfaz = iniciar("streamlit", ["run","src/app/inicio.py","--server.port","8501"])
            procesos.append(interfaz)
            for _ in range(100):
                if responde(ui + "/_stcore/health"):
                    break
                if interfaz.poll() is not None:
                    raise SystemExit("La interfaz local no pudo iniciar.")
                time.sleep(.2)
        if not responde(ui + "/_stcore/health"):
            raise SystemExit("La interfaz local no respondió a tiempo.")
        webbrowser.open(ui)
        if procesos:
            print("Consulta local disponible. Pulsa Ctrl+C para cerrar.")
            procesos[-1].wait()
    except KeyboardInterrupt:
        pass
    finally:
        for proceso in reversed(procesos):
            if proceso.poll() is None:
                proceso.terminate()
                proceso.wait()


if __name__ == "__main__":
    main()
