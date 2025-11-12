# 1001 Medya Kamera Sistemi - Deploy Kılavuzu

## ⚠️ ÖNEMLİ NOT

Bu bir **Flask uygulamasıdır** ve **Streamlit Cloud'a deploy edilemez**. Streamlit Cloud sadece Streamlit uygulamalarını destekler.

## Desteklenen Platformlar

### 1. Render.com (Önerilen - Ücretsiz)

1. [Render.com](https://render.com) hesabı oluşturun
2. GitHub repository'nizi bağlayın: `https://github.com/Neogtt/1001kamera`
3. Yeni Web Service oluşturun
4. Ayarlar:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3
   - **Plan**: Free

Render otomatik olarak `render.yaml` dosyasını kullanacaktır.

### 2. Railway.app

1. [Railway.app](https://railway.app) hesabı oluşturun
2. GitHub repository'nizi bağlayın
3. Yeni proje oluşturun
4. Railway otomatik olarak `Procfile` dosyasını kullanacaktır

### 3. Heroku

1. [Heroku](https://heroku.com) hesabı oluşturun
2. Heroku CLI ile:
```bash
heroku create 1001medya-kamera
git push heroku main
```

## Local Development

```bash
cd ~/1001Medya
pip install -r requirements.txt
python app.py
```

## Production Gereksinimleri

- Python 3.9+
- Gunicorn (WSGI server)
- OpenCV (headless versiyonu - GUI gerektirmez)

## Notlar

- Kamera stream'leri production'da çalışabilir ancak performans ağ bağlantısına bağlıdır
- RTSP stream'ler için güvenlik duvarı ayarlarını kontrol edin
- `cameras.json` dosyası production'da environment variable olarak saklanmalıdır
