"""Puntuar respuestas anónimas y tareas efectivamente observadas."""
import csv

from src import config

TAREAS = ("consulta", "comparacion", "boletin")
IDS = [f"P{i}" for i in range(1,6)]


def puntuar(respuestas):
    if len(respuestas) != 10 or any(v not in (1,2,3,4,5) for v in respuestas):
        raise ValueError("El SUS requiere diez respuestas enteras entre 1 y 5.")
    return 2.5 * sum(v-1 if i%2==0 else 5-v for i,v in enumerate(respuestas))


def leer(ruta):
    with ruta.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def exito(t):
    campos = ["completada","segundos","errores","ayuda","bloqueo_mas_120s"]
    if not all(t[k] for k in campos):
        return ""
    if any(t[k] not in {"si","no"} for k in ("completada","ayuda","bloqueo_mas_120s")):
        raise ValueError("Indique si o no en los campos de observación.")
    if int(t["segundos"]) < 0 or int(t["errores"]) < 0:
        raise ValueError("Tiempos y errores deben ser enteros no negativos.")
    return int(t["completada"]=="si" and t["ayuda"]=="no" and t["bloqueo_mas_120s"]=="no")


def main():
    docs = config.RAIZ / "docs"
    respuestas = leer(docs/"sus_respuestas.csv")
    tareas = leer(docs/"sus_tareas.csv")
    claves = [(t["participante"],t["tarea"]) for t in tareas]
    if sorted(r["participante"] for r in respuestas) != IDS or sorted(claves) != sorted((p,t) for p in IDS for t in TAREAS):
        raise ValueError("Se requieren P1–P5 y tres tareas únicas por código.")
    filas = []
    for r in respuestas:
        idp = r["participante"]
        consent = r["consentimiento"]
        if consent not in ("","si","no"):
            raise ValueError("Consentimiento válido: si, no o vacío.")
        valores = [r[f"i{i}"] for i in range(1,11)]
        if any(v and v not in {"1","2","3","4","5"} for v in valores):
            raise ValueError("Los ítems deben contener enteros de 1 a 5.")
        autorizado = consent=="si" and bool(r["perfil"])
        score = puntuar(list(map(int,valores))) if autorizado and all(valores) else ""
        estado = "retirado" if consent=="no" else "pendiente"
        resultados = {t["tarea"]: exito(t) if autorizado else "" for t in tareas if t["participante"]==idp}
        if autorizado:
            estado = "completo" if score!="" and all(v!="" for v in resultados.values()) else "incompleto"
        filas.append(dict(participante=idp,perfil=r["perfil"] if autorizado else "",estado=estado,sus=score,**resultados))
    completas = sum(r["estado"]=="completo" for r in filas)
    resumen = dict(participante="Resumen",perfil="",estado=f"{completas}/5 sesiones completas")
    for campo in ("sus",*TAREAS):
        valores = [r[campo] for r in filas if r[campo]!=""]
        resumen[campo] = (round(sum(valores)/len(valores),2) if campo=="sus"
                          else f"{sum(valores)}/{len(valores)}") if valores else ""
    ruta = config.REPORTES/"sus.csv"
    with ruta.open("w",encoding="utf-8",newline="") as f:
        csvw=csv.DictWriter(f,fieldnames=filas[0].keys())
        csvw.writeheader()
        csvw.writerows([*filas,resumen])


if __name__ == "__main__":
    main()
