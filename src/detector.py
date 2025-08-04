import cv2
import numpy as np

def detect_shaded_emergency_lights(image):
    """Detects dark, filled-in rectangular shapes from an image."""
    image_cv = np.array(image.convert('L'))
    _, thresh = cv2.threshold(image_cv, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    emergency_lights = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        
        # Simple filters for size and aspect ratio
        if area > 100 and w > 10 and h > 10 and 0.5 < w/h < 2.0:
            emergency_lights.append({'bbox': [x, y, x+w, y+h], 'area': area})

    return emergency_lights

