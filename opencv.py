import cv2
import requests
import numpy as np
from ultralytics import YOLO

# Load model
model = YOLO("yolo11n.pt")

url = "http://172.24.83.82:81/stream"

print("✅ Mencoba mengambil stream dengan metode HTTP...")

# Kita gunakan requests untuk bypass OpenCV VideoCapture yang bermasalah
stream = requests.get(url, stream=True)

if stream.status_code != 200:
    print("❌ Gagal akses stream. Cek IP atau koneksi.")
    exit()

bytes_data = bytes()
for chunk in stream.iter_content(chunk_size=1024):
    bytes_data += chunk
    a = bytes_data.find(b'\xff\xd8') # Awal JPEG
    b = bytes_data.find(b'\xff\xd9') # Akhir JPEG
    
    if a != -1 and b != -1:
        jpg = bytes_data[a:b+2]
        bytes_data = bytes_data[b+2:]
        
        # Decode ke format OpenCV
        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            # Jalankan YOLO
            results = model(frame, stream=True, conf=0.4, verbose=False)

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    label = f"{model.names[cls]} {conf:.2f}"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow("ESP32-CAM YOLOv11 (Arch Linux)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()