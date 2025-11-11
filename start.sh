#!/bin/bash

# 1001 Medya Kamera Yönetim Sistemi Başlatma Scripti

echo "1001 Medya - Kamera Yönetim Sistemi başlatılıyor..."
echo ""

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı aktifleştir
echo "Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Bağımlılıkları yükle
echo "Bağımlılıklar yükleniyor..."
pip install -r requirements.txt

# Uygulamayı başlat
echo ""
echo "Uygulama başlatılıyor..."
echo "Tarayıcınızda http://localhost:5000 adresini açın"
echo ""
python app.py

