import cv2
from ultralytics import YOLO

# Cek OpenCV
print(f"OpenCV Version: {cv2.__version__}")

# Cek YOLO
model = YOLO("yolov8n.pt")  # Ini akan otomatis mendownload weights
print("YOLO siap digunakan!")