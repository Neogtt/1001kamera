# 1001 Medya - Kamera Yönetim Sistemi

Video kameralara bağlanmak ve görüntülemek için web tabanlı bir arayüz.

## Özellikler

- 🔴 RTSP, HTTP ve IP Webcam desteği
- 📹 Çoklu kamera görüntüleme
- ➕ Kolay kamera ekleme
- 🔧 Kamera ayarları yönetimi
- 🧪 Kamera bağlantı testi
- 💾 Kamera konfigürasyonlarının otomatik kaydedilmesi

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:
```bash
python app.py
```

   Veya masaüstündeki `1001Medya_Kamera_Baslat.command` dosyasına çift tıklayın.

3. Tarayıcınızda şu adresi açın (port numarası terminal çıktısında gösterilir):
```
http://localhost:8080
```

**Not:** Uygulama otomatik olarak boş bir port bulur (varsayılan: 8080). Eğer port 5000 kullanılıyorsa (macOS'ta AirPlay Receiver), uygulama otomatik olarak 8080 portunu kullanır.

## Kullanım

### Kamera Ekleme

1. "Yeni Kamera Ekle" butonuna tıklayın
2. Kamera bilgilerini girin:
   - **Kamera Adı**: Kameranın görünen adı
   - **Kamera Tipi**: RTSP, HTTP, IP Webcam veya Yerel Kamera
   - **Kamera URL/Adresi**: Kamera stream adresi
   - **Kullanıcı Adı/Şifre**: Gerekirse kimlik doğrulama bilgileri
   - **Genişlik/Yükseklik/FPS**: İsteğe bağlı video ayarları

### RTSP Kamera Örneği
```
rtsp://192.168.1.100:554/stream
```

### HTTP Stream Örneği
```
http://192.168.1.100:8080/video
```

### IP Webcam Örneği
```
http://192.168.1.100:4747/video
```

## Kamera Tipleri

- **RTSP**: IP kameralar için standart protokol
- **HTTP**: HTTP üzerinden video stream
- **IP Webcam**: Mobil uygulamalardan gelen stream'ler
- **Yerel Kamera**: Bilgisayara bağlı USB/webcam

## Dosya Yapısı

```
1001-medya-kamera-arayuzu/
├── app.py                 # Flask backend
├── templates/
│   └── index.html        # Frontend arayüz
├── cameras.json          # Kamera konfigürasyonları (otomatik oluşturulur)
├── requirements.txt      # Python bağımlılıkları
└── README.md            # Bu dosya
```

## Notlar

- Kameralar `cameras.json` dosyasında saklanır
- Stream'ler MJPEG formatında servis edilir
- Her kamera için ayrı thread kullanılır
- Kamera bağlantıları otomatik olarak yönetilir

## Sorun Giderme

### Kamera bağlantısı kurulamıyor
- Kamera URL'sinin doğru olduğundan emin olun
- Kullanıcı adı ve şifrenin doğru olduğundan emin olun
- Ağ bağlantınızı kontrol edin
- Kamera ayarlarında port ve protokolün doğru olduğundan emin olun

### Görüntü gelmiyor
- "Test" butonuna tıklayarak kamera bağlantısını test edin
- Kamera stream formatının desteklendiğinden emin olun
- Tarayıcı konsolunda hata mesajlarını kontrol edin

## Lisans

1001 Medya için özel olarak geliştirilmiştir.

