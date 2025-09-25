from ultralytics import YOLO
import cv2

def run_object_detection():
    # Load YOLOv8 model (small model for speed)
    model = YOLO("yolov8n.pt")

    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return

    print("Starting object detection. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame")
            break

        # Run detection on the frame
        results = model(frame)[0]

        # Draw boxes on the frame
        annotated_frame = results.plot()

        # Show the frame with detections
        cv2.imshow("Object Detection", annotated_frame)

        # Quit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_object_detection()
