@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Bygger sajten ===
python build.py
if errorlevel 1 (
  echo.
  echo Bygget misslyckades, se felen ovan. Inget har publicerats.
  pause
  exit /b 1
)
echo.
echo === Publicerar till GitHub ===
git add -A
git commit -m "Uppdatering %date% %time:~0,5%" || echo (inga andringar att publicera)
git push
if errorlevel 1 (
  echo.
  echo Push misslyckades. Kontrollera internet och GitHub-inloggning (gh auth status).
  pause
  exit /b 1
)
echo.
echo Klart. GitHub Pages uppdaterar sajten inom nagon minut.
pause
