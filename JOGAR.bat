@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 game.py
) else (
  python game.py
)
if errorlevel 1 echo Verifique se o Python 3.10 ou superior esta instalado.
pause
