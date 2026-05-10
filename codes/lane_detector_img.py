import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Load the original image
image_c = cv2.imread('laneimg.jpeg')
image_c = cv2.cvtColor(image_c, cv2.COLOR_BGR2RGB) # Convert to RGB for Matplotlib

# 2. Pre-processing
image_g = cv2.cvtColor(image_c, cv2.COLOR_RGB2GRAY)
image_blurred = cv2.GaussianBlur(image_g, (7, 7), 0)
image_canny = cv2.Canny(image_blurred, 10, 200)

# 3. Define and Apply Region of Interest (ROI) Mask
vertices = np.array([[(100, 560), (440, 320), (540, 320), (890, 560)]], dtype=np.int32)
mask = np.zeros_like(image_g)
cv2.fillPoly(mask, vertices, 255)
masked_image = cv2.bitwise_and(image_canny, mask)

# 4. Hough Line Probabilistic Transform
# Unlike the standard version, HoughLinesP returns the actual endpoints (x1, y1, x2, y2)
rho = 2
theta = np.pi/180
threshold = 40
min_line_len = 100
max_line_gap = 50

lines = cv2.HoughLinesP(masked_image, rho, theta, threshold, np.array([]), 
                        minLineLength=min_line_len, maxLineGap=max_line_gap)

# 5. Draw the lines on a blank "canvas"
line_image = np.zeros_like(image_c)
if lines is not None:
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), [255, 0, 0], 10)

# 6. Merge the lines with the original image
# addWeighted blends the original image and the line canvas
final_image = cv2.addWeighted(image_c, 0.8, line_image, 1.0, 0.0)

# Display result
plt.imshow(final_image)
plt.title("Detected Lanes")
plt.show()
