import time
import board
import busio
import adafruit_mlx90640
import numpy as np
import cv2

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA, frequency=4000000)

# Initialize MLX90640 camera
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ
mlx_shape = (24, 32)

# Wait for MLX90640 to stabilize
time.sleep(5)

# Initialize OpenCV video window
cv2.namedWindow("Thermal Camera", cv2.WINDOW_NORMAL)

while True:
    # Capture frame from MLX90640 camera
    frame = np.zeros(mlx_shape[0]*mlx_shape[1])
    try:
        mlx.getFrame(frame)
    except ValueError:
        continue
    
    # Reshape MLX90640 frame into 2D array and convert to Celsius
    frame = np.reshape(frame, mlx_shape)
    frame = frame - 273.15
    
    # Apply outlier filtering
    sorted_frame = np.sort(frame, axis=None)
    min_val = sorted_frame[int(sorted_frame.size*0.01)]
    max_val = sorted_frame[int(sorted_frame.size*0.99)]
    frame = np.clip(frame, min_val, max_val)
    
    # Scale frame to 8-bit for display
    frame = (frame - min_val) / (max_val - min_val) * 255
    frame = np.uint8(frame)
    
    # Apply color map to frame
    frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
    
    # Display frame in OpenCV window
    cv2.imshow("Thermal Camera", frame)
    
    # Exit if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
