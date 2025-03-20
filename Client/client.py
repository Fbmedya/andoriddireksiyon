import requests
import time
import threading
import androidhelper

# **Froxy Medya Oyun Hizmetleri**
print("\n🚗 Froxy Medya Oyun Hizmetleri: Direksiyon Sistemi Başlatılıyor...\n")

# **Otomatik Sunucu Arama**
def find_server():
    base_ip = "192.168.1."  # Yerel ağ için
    for i in range(100, 150):  # 100 ile 150 arasındaki IP'leri tarayacak
        server_ip = f"{base_ip}{i}"
        try:
            response = requests.get(f"http://{server_ip}:5000/status", timeout=0.3)
            if response.status_code == 200:
                print(f"✅ Sunucu Bulundu: {server_ip}")
                return server_ip
        except:
            pass
    print("❌ Sunucu Bulunamadı! Manuel IP Giriniz.")
    return None

# **Sunucu Bağlantısı**
SERVER_IP = find_server() or input("📡 Sunucu IP Girin: ")
print(f"🔗 Bağlanılan Sunucu: {SERVER_IP}")

# **Sistem Ayarları**
max_steering_angle = 450.0
steering_angle = 0.0
delta_time = 0.05  # 50ms gecikme
gyro_sensitivity = 30

# **Android Jiroskop Başlat**
droid = androidhelper.Android()

def send_steering_angle(angle):
    """Direksiyon açısını sunucuya gönder"""
    url = f'http://{SERVER_IP}:5000/set_steering_angle'
    try:
        payload = {'angle': f"{angle:.2f}"}
        requests.post(url, data=payload, timeout=0.2)
    except:
        pass

def get_steering_angle():
    """Sunucudan direksiyon açısını al"""
    url = f'http://{SERVER_IP}:5000/get_steering_angle'
    try:
        response = requests.get(url, timeout=0.2)
        return float(response.text.strip())
    except:
        return None

def read_gyroscope():
    """Telefonun jiroskop verisini oku"""
    try:
        event = droid.sensorsReadGyroscope().result
        return event if event else (0.0, 0.0, 0.0)
    except:
        return (0.0, 0.0, 0.0)

def steering_loop():
    """Jiroskop verisini direksiyon açısına dönüştürme"""
    global steering_angle
    while True:
        gyro_x, gyro_y, gyro_z = read_gyroscope()
        steering_angle += gyro_z * gyro_sensitivity * delta_time
        steering_angle = max(-max_steering_angle, min(max_steering_angle, steering_angle))

        send_steering_angle(steering_angle)
        current_angle = get_steering_angle()
        if current_angle is not None:
            print(f"🎮 Direksiyon Açısı: {current_angle:.2f}°")

        time.sleep(delta_time)

# **Arka Planda Direksiyon Sistemi Çalıştır**
thread = threading.Thread(target=steering_loop, daemon=True)
thread.start()

print("\n✅ Froxy Medya Direksiyon Sistemi Aktif! 🚀")
