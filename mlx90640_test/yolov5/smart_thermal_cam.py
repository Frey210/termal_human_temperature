import subprocess
import cv2
import numpy as np

# Path to bash file that calls yolov5 program
bash_path = '/path/to/bash/file.sh'

# Run bash file to detect humans in thermal image and crop the image
process = subprocess.Popen(bash_path.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

# Load cropped image
img = cv2.imread('cropped_image.jpg')

# Calculate average temperature of cropped image
temp_array = cv2.imread('thermal_image.jpg', cv2.IMREAD_GRAYSCALE)
temp_crop = temp_array[y:y+h, x:x+w] # Replace x, y, w, h with values from detection
avg_temp = np.mean(temp_crop) / 100

# Print the average temperature of the cropped image
print('Average temperature: {} C'.format(avg_temp))