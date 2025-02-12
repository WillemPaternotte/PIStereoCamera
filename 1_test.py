import time
import cv2
import numpy as np
from picamera2 import Picamera2

def start_camera(camera_id):
    """Initialize and start the camera stream."""
    picam2 = Picamera2(camera_num=camera_id)
    config = picam2.create_video_configuration()
    picam2.configure(config)
    picam2.start()
    time.sleep(1)  # Allow time for the camera to adjust
    return picam2

# Start both cameras
camera1 = start_camera(0)
camera2 = start_camera(1)

while True:
    # Capture frames from both cameras
    frame1 = camera1.capture_array()
    frame2 = camera2.capture_array()

    if frame1 is None or frame2 is None:
        print("Error: Could not capture frames.")
        break

    # Convert to OpenCV BGR format
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR)

    # Resize frames to ensure they match in height
    # height = min(frame1.shape[0], frame2.shape[0])
    # frame1 = cv2.resize(frame1, (frame1.shape[1], height))
    # frame2 = cv2.resize(frame2, (frame2.shape[1], height))

    # Combine frames side by side
    combined_frame = cv2.hconcat([frame1, frame2])
    combined_frame =  cv2.resize(combined_frame, (1920, 640))
    
    # Display the video stream
    cv2.imshow("Camera 0 and Camera 1", combined_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
camera1.stop()
camera2.stop()
cv2.destroyAllWindows()
