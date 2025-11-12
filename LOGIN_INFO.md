# Giriş Sistemi Bilgileri

## Varsayılan Kullanıcı

**E-posta:** `admin@1001medya.com`  
**Şifre:** `admin123`

## Özellikler

- ✅ Modern ve güvenli giriş ekranı
- ✅ Session tabanlı authentication
- ✅ Tüm kamera sayfaları korumalı
- ✅ Çıkış yapma özelliği
- ✅ Şifre görünürlük toggle'ı

## Güvenlik Notları

⚠️ **Production'da mutlaka:**
- `SECRET_KEY` environment variable'ını değiştirin
- Kullanıcı şifrelerini veritabanında saklayın
- Şifreleri bcrypt gibi güvenli hash algoritmalarıyla hash'leyin
- HTTPS kullanın

## Kullanım

1. Uygulamayı başlatın
2. Tarayıcıda `/login` sayfasına gidin
3. Varsayılan kullanıcı bilgileriyle giriş yapın
4. Kamera yönetim sistemine erişin

## Yeni Kullanıcı Ekleme

Şu anda kullanıcılar `app.py` dosyasındaki `USERS` dictionary'sinde tanımlıdır. Production'da veritabanı kullanılmalıdır.

