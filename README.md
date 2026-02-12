
### Panduan Instalasi

### 1. Persiapan Firmware (ESP32)
- Buka file di folder `firmware/esp32_stream.ino` menggunakan Arduino IDE.
- Sesuaikan `SSID` dan `PASSWORD` WiFi Anda.
- Flash ke ESP32-CAM dan pastikan jumper `IO0` dilepas setelah selesai.

### 2. Persiapan Python Environment
```bash
# Clone project
git clone [https://github.com/kangleem/deteksi-object.git](https://github.com/username/ESP32CAM-YOLO-Stream.git)
cd my_yolo

# Buat virtual environment
python -m venv venv
source venv/bin/activate.fish //jika tidak menggunakan fish, hapus .fish

# Install dependensi
pip install ultralytics flask opencv-python requests
