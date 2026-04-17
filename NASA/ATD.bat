@echo off
chcp 65001 >nul
echo =============================================================
echo   System pro analyzu a predikci nebezpecnych asteroidu (ATA)
echo =============================================================
echo.

echo Krok 1: Kontroluji a vytvarim izolovanou bublinu (venv)...
echo (Ochrana pred nutnosti mit administratorska prava)
if not exist "venv\" (
    python -m venv venv
)

echo.
echo Krok 2: Aktivuji bublinu a overuji potrebne knihovny...
call venv\Scripts\activate
python -m pip install --upgrade pip >nul
pip install -r docs\requirements.txt

echo.
echo Krok 3: Spoustim aplikaci...
python src\Aplikace.py

echo.
echo Aplikace byla ukoncena.
pause
