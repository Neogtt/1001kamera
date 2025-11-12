from flask import Flask, render_template, jsonify, request, Response, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
import cv2
import threading
import json
import os
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '1001medya-secret-key-change-in-production')
CORS(app)

# Basit kullanıcı sistemi (production'da veritabanı kullanılmalı)
USERS = {
    'admin@1001medya.com': {
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),  # Şifre: admin123
        'name': 'Admin'
    }
}

def login_required(f):
    """Login gerektiren route'lar için decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Kamera yönetimi
cameras = {}
camera_configs = {}
camera_lock = threading.Lock()

# Kamera konfigürasyon dosyası
CONFIG_FILE = 'cameras.json'

def load_camera_configs():
    """Kamera konfigürasyonlarını yükle"""
    global camera_configs
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                camera_configs = json.load(f)
        except Exception as e:
            print(f"Konfigürasyon yüklenirken hata: {e}")
            camera_configs = {}

def save_camera_configs():
    """Kamera konfigürasyonlarını kaydet"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(camera_configs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Konfigürasyon kaydedilirken hata: {e}")

def get_camera_stream(camera_id):
    """Kamera stream'ini al"""
    config = camera_configs.get(camera_id)
    if not config:
        return None
    
    try:
        url = config.get('url', '')
        
        if config['type'] == 'rtsp':
            # RTSP için buffer ayarları
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Buffer'ı küçült, gecikmeyi azalt
        elif config['type'] == 'http':
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        elif config['type'] == 'ip_webcam':
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        else:
            # Yerel kamera
            cap = cv2.VideoCapture(int(config.get('index', 0)))
        
        # Bağlantı kontrolü
        if not cap.isOpened():
            print(f"Kamera açılamadı: {camera_id}")
            return None
        
        # Kamera ayarları
        if config.get('width'):
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['width'])
        if config.get('height'):
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['height'])
        if config.get('fps'):
            cap.set(cv2.CAP_PROP_FPS, config['fps'])
        
        # Timeout ayarı (RTSP için)
        if config['type'] == 'rtsp':
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
            cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)
        
        return cap
    except Exception as e:
        print(f"Kamera açılırken hata ({camera_id}): {e}")
        return None

def generate_frames(camera_id):
    """Video frame'lerini üret"""
    cap = None
    max_retries = 3
    retry_count = 0
    
    while True:
        # Kamera hala konfigürasyonda mı kontrol et
        with camera_lock:
            if camera_id not in camera_configs:
                if cap:
                    cap.release()
                break
        
        # Kamera bağlantısı yoksa veya kapanmışsa yeniden bağlan
        if cap is None or not cap.isOpened():
            if retry_count >= max_retries:
                break
            cap = get_camera_stream(camera_id)
            if cap is None or not cap.isOpened():
                retry_count += 1
                import time
                time.sleep(2)  # 2 saniye bekle
                continue
            retry_count = 0
        
        # Frame oku
        ret, frame = cap.read()
        if not ret:
            # Frame alınamadı, kamerayı kapat ve yeniden dene
            if cap:
                cap.release()
            cap = None
            retry_count += 1
            continue
        
        # Frame'i JPEG'e çevir
        try:
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                continue
            
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except Exception as e:
            print(f"Frame encode hatası ({camera_id}): {e}")
            continue
    
    # Temizlik
    if cap:
        cap.release()

@app.route('/login')
def login():
    """Giriş sayfası"""
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """Giriş API endpoint'i"""
    data = request.json
    email = data.get('email', '').lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'E-posta ve şifre gereklidir'}), 400
    
    # Kullanıcı kontrolü
    if email in USERS:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if USERS[email]['password'] == hashed_password:
            session['user'] = email
            session['name'] = USERS[email]['name']
            return jsonify({'success': True, 'message': 'Giriş başarılı'})
    
    return jsonify({'success': False, 'message': 'E-posta veya şifre hatalı'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Çıkış API endpoint'i"""
    session.clear()
    return jsonify({'success': True, 'message': 'Çıkış yapıldı'})

@app.route('/')
@login_required
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/cameras', methods=['GET'])
@login_required
def get_cameras():
    """Tüm kameraları listele"""
    cameras_list = []
    for camera_id, config in camera_configs.items():
        cameras_list.append({
            'id': camera_id,
            'name': config.get('name', 'İsimsiz Kamera'),
            'type': config.get('type', 'unknown'),
            'url': config.get('url', ''),
            'status': 'active' if camera_id in cameras else 'inactive',
            'created_at': config.get('created_at', '')
        })
    return jsonify(cameras_list)

@app.route('/api/cameras', methods=['POST'])
@login_required
def add_camera():
    """Yeni kamera ekle"""
    data = request.json
    
    camera_id = data.get('id') or f"camera_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    camera_configs[camera_id] = {
        'name': data.get('name', 'Yeni Kamera'),
        'type': data.get('type', 'rtsp'),  # rtsp, http, ip_webcam, local
        'url': data.get('url', ''),
        'index': data.get('index', 0),
        'width': data.get('width'),
        'height': data.get('height'),
        'fps': data.get('fps'),
        'username': data.get('username'),
        'password': data.get('password'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # URL'de kullanıcı adı ve şifre varsa ekle
    if camera_configs[camera_id]['username'] and camera_configs[camera_id]['password']:
        url = camera_configs[camera_id]['url']
        if '://' in url:
            protocol = url.split('://')[0]
            url_without_protocol = url.split('://')[1]
            camera_configs[camera_id]['url'] = f"{protocol}://{camera_configs[camera_id]['username']}:{camera_configs[camera_id]['password']}@{url_without_protocol}"
    
    save_camera_configs()
    
    # Kamerayı başlat
    cameras[camera_id] = True
    
    return jsonify({
        'success': True,
        'message': 'Kamera başarıyla eklendi',
        'camera_id': camera_id
    })

@app.route('/api/cameras/<camera_id>', methods=['DELETE'])
@login_required
def delete_camera(camera_id):
    """Kamerayı sil"""
    if camera_id in camera_configs:
        del camera_configs[camera_id]
        if camera_id in cameras:
            del cameras[camera_id]
        save_camera_configs()
        return jsonify({'success': True, 'message': 'Kamera silindi'})
    return jsonify({'success': False, 'message': 'Kamera bulunamadı'}), 404

@app.route('/api/cameras/<camera_id>', methods=['PUT'])
@login_required
def update_camera(camera_id):
    """Kamerayı güncelle"""
    if camera_id not in camera_configs:
        return jsonify({'success': False, 'message': 'Kamera bulunamadı'}), 404
    
    data = request.json
    camera_configs[camera_id].update(data)
    save_camera_configs()
    
    return jsonify({'success': True, 'message': 'Kamera güncellendi'})

@app.route('/video_feed/<camera_id>')
@login_required
def video_feed(camera_id):
    """Video stream endpoint'i"""
    if camera_id not in camera_configs:
        return "Kamera bulunamadı", 404
    
    return Response(generate_frames(camera_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/cameras/<camera_id>/test', methods=['POST'])
@login_required
def test_camera(camera_id):
    """Kamera bağlantısını test et"""
    config = camera_configs.get(camera_id)
    if not config:
        return jsonify({'success': False, 'message': 'Kamera bulunamadı'}), 404
    
    cap = get_camera_stream(camera_id)
    if cap is None or not cap.isOpened():
        return jsonify({'success': False, 'message': 'Kamera bağlantısı başarısız'})
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        return jsonify({'success': True, 'message': 'Kamera bağlantısı başarılı'})
    else:
        return jsonify({'success': False, 'message': 'Kamera görüntü alınamadı'})

if __name__ == '__main__':
    load_camera_configs()
    import socket
    import os
    
    # Production'da PORT environment variable'ını kullan
    port = int(os.environ.get('PORT', 8080))
    
    # Development'ta port bulma
    if port == 8080 and os.environ.get('FLASK_ENV') != 'production':
        def find_free_port(start_port=8080):
            port = start_port
            while port < start_port + 100:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        sock.bind(('127.0.0.1', port))
                        return port
                except OSError:
                    port += 1
            return 8080
        port = find_free_port(8080)
    
    print(f"\n{'='*60}")
    print(f"🚀 Server başlatılıyor...")
    print(f"🌐 Tarayıcınızda şu adresi açın: http://localhost:{port}")
    print(f"{'='*60}\n")
    
    # Production'da debug kapalı
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port, threaded=True)

