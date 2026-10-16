@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Bygger sajten ===
python build.py
if errorlevel 1 (
  echo Bygget misslyckades, inget har laddats upp.
  pause
  exit /b 1
)
findstr /C:"STAGING = True" build.py >nul
if not errorlevel 1 (
  echo.
  echo STOPP: STAGING = True i build.py. Sajten skulle laddas upp med noindex och spärrad robots.txt.
  echo Sätt STAGING = False i build.py innan du publicerar till Loopia.
  pause
  exit /b 1
)
echo.
echo === Laddar upp till Loopia via FTP ===
python tools\ladda_upp_ftp.py
if errorlevel 1 (
  echo Uppladdningen misslyckades, se felet ovan.
  pause
  exit /b 1
)
echo.
echo === Sparar även i GitHub ===
git add -A
git commit -m "Publicerad till Loopia %date% %time:~0,5%" || echo (inga ändringar att spara)
git push
pause
