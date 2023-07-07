import cv2
import numpy as np

# load image and detection results
image = cv2.imread('temp_image.jpg')
detections = np.loadtxt('detections.txt', delimiter=',')

# filter out detections for humans only
humans = detections[detections[:, 5] == 0]

# crop image for each human detection and calculate temperature
for i, human in enumerate(humans):
    x1, y1, x2, y2 = human[:4].astype(int)
    human_image = image[y1:y2, x1:x2]
    human_temp = np.mean(human_image)  # calculate temperature based on mean pixel value
    print(f"Human {i+1} temperature: {human_temp:.2f} C")
