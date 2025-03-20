import time
import math
from flask import Flask, request

app = Flask(__name__)

# **Direksiyon Açısı**
steering_angle = 0.0
max_steering_angle = 450.0

@app.route('/set_steering_angle', methods=['POST'])
def set_steering_angle():
    """Gelen direksiyon açısını kaydet"""
    global steering_angle
    try:
        angle = float(request.form['angle'])
        steering_angle = max(-max_steering_angle, min(max_steering_angle, angle))
        print(f"🔄 Direksiyon Açısı: {steering_angle:.2f}°")
        return 'OK'
    except ValueError:
        return 'Hatalı Veri', 400

@app.route('/get_steering_angle', methods=['GET'])
def get_steering_angle():
    """Direksiyon açısını gönder"""
    return str(steering_angle)

@app.route('/status', methods=['GET'])
def status():
    """Sunucunun çalıştığını gösteren basit bir yanıt"""
    return "OK"

@app.before_request
def log_ip():
    """Bağlanan cihazın IP adresini kaydet"""
    ip = request.remote_addr
    print(f"📡 Bağlanan Cihaz IP: {ip}")

if __name__ == '__main__':
    print("🚀 Froxy Medya Oyun Sunucusu Başlatılıyor...")
    app.run(host='0.0.0.0', port=5000, debug=True)
