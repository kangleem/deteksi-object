# 📷 ESP32-CAM Real-Time Object Detection with YOLOv11 & Ngrok

Proyek ini adalah sistem pemantauan cerdas berbasis AI yang menghubungkan **ESP32-CAM** dengan model **YOLOv11** di Linux. Video dikirimkan dari ESP32-CAM, diproses oleh server lokal untuk deteksi objek, dan dipublikasikan ke internet menggunakan **Ngrok**.



## 🌟 Fitur Utama
- **Stream Stabil & Ringan**: Firmware ESP32 dioptimalkan untuk pengiriman MJPEG tanpa beban dashboard HTML yang berat.
- **YOLOv11 Integration**: Menggunakan versi YOLO terbaru (v11) untuk akurasi dan kecepatan maksimal.
- **Multi-threaded Processing**: Python menggunakan teknik threading untuk memastikan stream video bersifat real-time (anti-lag).
- **Global Access**: Berkat Flask dan Ngrok, hasil deteksi dapat dipantau dari jaringan internet mana pun (HP/Laptop luar kota).
- **Auto-Lighting**: Konfigurasi otomatis pada sensor kamera agar tetap terang di kondisi cahaya rendah.

## 🏗️ Arsitektur Sistem
1. **ESP32-CAM**: Mengambil gambar dan mengirimkan stream MJPEG melalui WiFi lokal.
2. **Local Server (Arch Linux)**: Menangkap stream, menjalankan inferensi YOLOv11, dan menggambar bounding boxes.
3. **Flask Web Server**: Membungkus hasil deteksi ke dalam antarmuka web.
4. **Ngrok Tunnel**: Membuat jalur aman (HTTPS) agar server lokal dapat diakses secara publik.



## 🛠️ Persyaratan Sistem
- **Hardware**: ESP32-CAM (AI-Thinker), Kabel FTDI (untuk flash), Powerbank/Charger HP.
- **Software**: 
  - Arch Linux (atau distro Linux lainnya)
  - Python 3.10+
  - Arduino IDE (untuk upload firmware)

## 📦 Panduan Instalasi

### 1. Persiapan Firmware (ESP32)
- Buka file di folder `firmware/esp32_stream.ino` menggunakan Arduino IDE.
- Sesuaikan `SSID` dan `PASSWORD` WiFi Anda.
- Flash ke ESP32-CAM dan pastikan jumper `IO0` dilepas setelah selesai.

### 2. Persiapan Python Environment
```bash
# Clone project
git clone [https://github.com/username/ESP32CAM-YOLO-Stream.git](https://github.com/username/ESP32CAM-YOLO-Stream.git)
cd ESP32CAM-YOLO-Stream

# Buat virtual environment
python -m venv venv
source venv/bin/activate

# Install dependensi
pip install ultralytics flask opencv-python requests
