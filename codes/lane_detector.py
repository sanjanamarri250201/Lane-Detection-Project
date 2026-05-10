import cv2
import numpy as np

def process_frame(frame):
    # 1. Grayscale & Blur
    # We remove color to simplify edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 2. Canny Edge Detection
    # Detects sharp changes in intensity
    canny = cv2.Canny(blur, 50, 150)

    # 3. Define Region of Interest (ROI)
    # This creates a triangle/trapezoid mask to ignore the sky/trees
    height, width = canny.shape
    mask = np.zeros_like(canny)
    
    # Adjust these coordinates if your video has a different perspective
    vertices = np.array([[(0, height), (width//2 - 50, height//2 + 50), 
                          (width//2 + 50, height//2 + 50), (width, height)]], dtype=np.int32)
    
    cv2.fillPoly(mask, vertices, 255)
    masked_edges = cv2.bitwise_and(canny, mask)

    # 4. Probabilistic Hough Transform
    # Finds line segments from the edge-detected pixels
    lines = cv2.HoughLinesP(masked_edges, 2, np.pi/180, 100, 
                            np.array([]), minLineLength=40, maxLineGap=25)

    # 5. Drawing the lines
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)

    # 6. Weighted Overlay
    # Merges the lines with the original color frame
    return cv2.addWeighted(frame, 0.8, line_image, 1, 0)

def main():
    # Load your video file
    video_path = 'video.mp4' 
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open {video_path}. Make sure it's in the same folder.")
        return

    print("Processing... Press 'q' to exit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame through our pipeline
        result = process_frame(frame)

        # Show the result in a window
        cv2.imshow('Lane Detection Project', result)

        # 'q' key to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
