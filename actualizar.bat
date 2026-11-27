@echo off
setlocal
cd /d "%~dp0"
call ".venv\Scripts\activate.bat" || exit /b 1
python -m scripts.verificar_bronce || exit /b 1
python -m src.pipeline || exit /b 1
python -m src.models || exit /b 1
python -m src.app.precalcular || exit /b 1
