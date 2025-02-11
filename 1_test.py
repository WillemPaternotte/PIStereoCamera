import cv2
import numpy as np
from picamera2 import Picamera2

def capture_image(camera_id):
    """Capture an image from the specified camera and return it as a NumPy array."""
    picam2 = Picamera2(camera_num=camera_id)
    config = picam2.create_still_configuration()
    picam2.configure(config)
    
    picam2.start()
    image = picam2.capture_array()  # Directly get image as NumPy array
    picam2.stop()
    
    return image

# Capture images from both cameras
image1 = capture_image(0)
image2 = capture_image(1)

# Ensure images were captured successfully
if image1 is None or image2 is None:
    print("Error: Could not capture one or both images.")
else:
    # Convert images to OpenCV BGR format
    image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
    image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)

    # Combine images side by side
    combined_image = cv2.hconcat([image1, image2])

    # Display the images
    cv2.imshow("Camera 0 and Camera 1", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
