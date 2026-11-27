@echo off
setlocal
cd /d "%~dp0"
call ".venv\Scripts\activate.bat" || exit /b 1
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
python -m src.app.iniciar
exit /b %errorlevel%
