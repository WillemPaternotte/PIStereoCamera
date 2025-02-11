from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import os
from datetime import datetime

# User quit method message 
print("You can press 'Q' to quit this script.")

# File for captured image
filename = './scenes/photo.png'

# Camera settings
cam_width = 1280
cam_height = 480
scale_ratio = 0.5  # Final image capture settings

# Adjust resolution
cam_width = int((cam_width+31)/32)*32
cam_height = int((cam_height+15)/16)*16
print(f"Camera resolution: {cam_width} x {cam_height}")

# Scaled image settings
img_width = int(cam_width * scale_ratio)
img_height = int(cam_height * scale_ratio)
print(f"Scaled image resolution: {img_width} x {img_height}")

# Initialize the camera
picam2 = Picamera2()
config = picam2.create_still_configuration(
    main={'size': (cam_width, cam_height)},
    transform={'mirror': False},
    buffer_count=2
)
picam2.configure(config)
picam2.start()

# Performance tracking
t0 = datetime.now()
counter = 0

while True:
    frame = picam2.capture_array()  # Capture image as NumPy array
    frame_resized = cv2.resize(frame, (img_width, img_height))  # Resize frame
    
    cv2.imshow("pair", frame_resized)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        t1 = datetime.now()
        timediff = t1 - t0
        print(f"Frames: {counter} Time: {timediff.total_seconds()} Average FPS: {counter / timediff.total_seconds():.2f}")
        
        if not os.path.exists("./scenes"):
            os.makedirs("./scenes")
        
        cv2.imwrite(filename, frame_resized)
        break
    
    counter += 1

cv2.destroyAllWindows()
picam2.stop()
