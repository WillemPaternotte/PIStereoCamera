import cv2
import numpy as np
import subprocess

def capture_image(camera_index):
    """Capture an image from the specified camera and return it as a NumPy array."""
    command = [
        "libcamera-still",
        "--camera", str(camera_index),
        "-t", "1",
        "--nopreview",
        "--output", "-",  # Output to stdout instead of a file
        "--encoding", "jpeg"  # Ensure JPEG output
    ]

    # Run the command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    # Convert the output bytes to a NumPy array and decode it as an image
    image = cv2.imdecode(np.frombuffer(result.stdout, dtype=np.uint8), cv2.IMREAD_COLOR)
    return image

# Capture images from both cameras
image1 = capture_image(0)
image2 = capture_image(1)

# Check if images are valid
if image1 is None or image2 is None:
    print("Error: Could not capture one or both images.")
else:
    # Combine images side by side
    combined_image = cv2.hconcat([image1, image2])

    # Display the images
    cv2.imshow("Camera 0 and Camera 1", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
