import cv2
import requests
import numpy as np
from ultralytics import YOLO
from flask import Flask, Response
import time

app = Flask(__name__)

# Load model sekali saja saat startup
print("⏳ Loading YOLOv11...")
model = YOLO("yolo11n.pt")

# TIPS: Gunakan IP Lokal ESP32 jika Laptop & ESP32 di WiFi yang sama
# Ini jauh lebih stabil dan tidak membebani kuota Ngrok kamu.
ESP32_STREAM_URL = "http://192.168.1.38:81/stream" 

def generate_frames():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'ngrok-skip-browser-warning': 'true'
    }
    
    while True:
        try:
            # Mulai request stream
            stream = requests.get(ESP32_STREAM_URL, headers=headers, stream=True, timeout=10)
            
            if stream.status_code != 200:
                print(f"❌ Koneksi gagal, status: {stream.status_code}")
                time.sleep(2)
                continue

            bytes_data = bytes()
            for chunk in stream.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8') # Start JPEG
                b = bytes_data.find(b'\xff\xd9') # End JPEG
                
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b+2]
                    bytes_data = bytes_data[b+2:]
                    
                    # Decode gambar
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    if frame is not None:
                        # Jalankan YOLO
                        results = model(frame, stream=True, conf=0.3, verbose=False)
                        
                        for r in results:
                            for box in r.boxes:
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                cls = int(box.cls[0])
                                conf = float(box.conf[0])
                                label = f"{model.names[cls]} {conf:.2f}"
                                
                                # Gambar kotak & label
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, label, (x1, y1 - 10), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        # Encode ke JPEG untuk dikirim ke web
                        ret, buffer = cv2.imencode('.jpg', frame)
                        if not ret:
                            continue
                            
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        except Exception as e:
            print(f"⚠️ Error: {e}. Mencoba menghubungkan kembali...")
            time.sleep(2)

@app.route('/video_feed')
def video_feed():
    # Rute ini akan mengirimkan stream video mentah hasil olahan AI
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Rute utama untuk menampilkan halaman web simpel
    return """
    <html>
      <head>
        <title>ESP32-CAM YOLOv11</title>
        <style>
          body { font-family: sans-serif; text-align: center; background: #1a1a1a; color: white; }
          img { border: 5px solid #00ff00; border-radius: 10px; max-width: 90%; }
        </style>
      </head>
      <body>
        <h1>Live AI Object Detection</h1>
        <img src="/video_feed">
        <p>Status: Streaming Online</p>
      </body>
    </html>
    """

if __name__ == "__main__":
    # Menjalankan Flask di port 5000
    print("🚀 Server berjalan di http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, threaded=True)