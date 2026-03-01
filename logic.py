import cv2
import numpy as np
from ultralytics import YOLO

# Optimized for AMD ROCm stack inference
model = YOLO('yolov8n.pt') 

def get_risk_metrics(img_array):
    results = model(img_array, verbose=False)
    annotated_img = results[0].plot() 

    # Threat Classes: 43: knife, 76: scissors, 34: baseball bat
    threat_classes = [43, 76, 34] 
    detected_threats = [box for box in results[0].boxes if int(box.cls) in threat_classes]
    
    # Environmental Signals
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    darkness_score = 1 - (np.mean(gray) / 255)
    
    people = [box for box in results[0].boxes if int(box.cls) == 0]
    p_count = len(people)

    return {
        "darkness": darkness_score,
        "isolation": 1.0 if p_count == 0 else 0,
        "threat_detected": len(detected_threats) > 0,
        "count": p_count,
        "image": annotated_img,
        "raw_image": img_array 
    }
