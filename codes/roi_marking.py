import cv2
import numpy as np

# Load the video
cap = cv2.VideoCapture('video.mp4')

# 1. Initialize Adjustable Windows
cv2.namedWindow('Canny Edges', cv2.WINDOW_NORMAL)
cv2.namedWindow('Masked View', cv2.WINDOW_NORMAL)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    # Convert to grayscale and find edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 10, 200)
    
    # 2. Define the Region of Interest (ROI)
    # Note: These coordinates depend on your specific video resolution
    # You can adjust these points manually to fit your specific road view
    vertices = np.array([[(0, 800), (450, 400), (750, 400), (1400, 800)]], dtype=np.int32)
    
    # 3. Create and Apply the Mask
    mask = np.zeros_like(gray)
    cv2.fillPoly(mask, vertices, 255)
    
    # Bitwise AND keeps only the white edge pixels that fall inside the white mask polygon
    masked_image = cv2.bitwise_and(canny, mask)
    
    # 4. Display
    cv2.imshow('Canny Edges', canny)
    cv2.imshow('Masked View', masked_image)
  
    # Exit logic: 'q' key or clicking the 'X' button
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty('Canny Edges', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
