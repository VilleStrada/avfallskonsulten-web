@echo off
cd /d "%~dp0"
python build.py || (pause & exit /b 1)
start "" http://localhost:8765/
python tools\forhandsgranska.py 8765
