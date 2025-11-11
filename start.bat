@echo off
REM 1001 Medya Kamera Yönetim Sistemi Başlatma Scripti (Windows)

echo 1001 Medya - Kamera Yönetim Sistemi baslatiliyor...
echo.

REM Sanal ortam kontrolü
if not exist "venv" (
    echo Sanal ortam olusturuluyor...
    python -m venv venv
)

REM Sanal ortamı aktifleştir
echo Sanal ortam aktiflestiriliyor...
call venv\Scripts\activate.bat

REM Bağımlılıkları yükle
echo Bagimliliklar yukleniyor...
pip install -r requirements.txt

REM Uygulamayı başlat
echo.
echo Uygulama baslatiliyor...
echo Tarayicinizda http://localhost:5000 adresini acin
echo.
python app.py

pause

