import cv2

# Use 0 for built-in, 1 for external. 
cap = cv2.VideoCapture(0) 

# Define window names
windows = ['Original', 'Gray', 'Canny (Edges)', 'Blur']

# Initialize adjustable windows
for name in windows:
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # 1. Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. Gaussian Blur (reduces noise for better edge detection)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 3. Canny Edge Detection
    canny = cv2.Canny(blur, 50, 200)
    
    # Display frames
    cv2.imshow('Original', frame)
    cv2.imshow('Gray', gray)
    cv2.imshow('Blur', blur)
    cv2.imshow('Canny (Edges)', canny)
    
    # Wait for 1ms; exit if 'q' is pressed OR if a window is closed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or cv2.getWindowProperty('Original', cv2.WND_PROP_VISIBLE) < 1:
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
