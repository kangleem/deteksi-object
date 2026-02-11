import cv2
import requests
import numpy as np
from ultralytics import YOLO
import sys

# --- KONFIGURASI ---
# Ganti dengan URL Ngrok kamu saat ini (selalu tambahkan /stream di ujungnya)
# URL_NGROK = "https://untippable-unworked-braeden.ngrok-free.dev/stream"
URL_NGROK= "http://192.168.1.38:81/stream"

def run_detection():
    print("🔄 Memuat model YOLOv11...")
    try:
        model = YOLO("yolo11n.pt") # Otomatis download jika belum ada
    except Exception as e:
        print(f"❌ Gagal memuat model: {e}")
        return

    # Header Wajib untuk menembus proteksi Ngrok
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'ngrok-skip-browser-warning': 'true'
    }

    print(f"📡 Menghubungkan ke: {URL_NGROK}")

    try:
        # Stream=True menjaga koneksi tetap terbuka untuk menerima data berkelanjutan
        response = requests.get(URL_NGROK, headers=headers, stream=True, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Gagal! Status Code: {response.status_code}")
            return

        print("✅ Terhubung! Memulai deteksi objek...")
        bytes_data = bytes()

        for chunk in response.iter_content(chunk_size=1024):
            bytes_data += chunk
            # Mencari penanda awal (0xff 0xd8) dan akhir (0xff 0xd9) file JPEG
            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')
            
            if a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
                
                # Mengubah bytes menjadi format gambar OpenCV
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                if frame is not None:
                    # Jalankan YOLO (conf=0.3 artinya tingkat keyakinan minimal 30%)
                    results = model(frame, stream=True, conf=0.3, verbose=False)

                    for r in results:
                        for box in r.boxes:
                            # Ambil koordinat kotak
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            conf = float(box.conf[0])
                            cls = int(box.cls[0])
                            label = f"{model.names[cls]} {conf:.2f}"

                            # Gambar kotak hijau dan label teks
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, label, (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Tampilkan di jendela Arch Linux
                    cv2.imshow("YOLOv11 - ESP32-CAM (Ngrok)", frame)

                # Tekan 'q' untuk berhenti
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except Exception as e:
        print(f"❌ Error saat streaming: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_detection()