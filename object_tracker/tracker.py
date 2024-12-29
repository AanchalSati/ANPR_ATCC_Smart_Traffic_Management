from ultralytics import YOLO
import cv2
import random

class Tracker:
    def __init__(self):
        self.model = YOLO("yolov8x.pt")  

    def detect_objects(self, frames):
        detections = []
        for frame in frames:
            detected_objs = self.detect_frame(frame)
            detections.append(detected_objs)
        return detections

    def detect_frame(self, frame):
        results = self.model.track(frame, persist=True)[0]
        name_dict = results.names

        detected_objects = {}

        for box in results.boxes:
            track_id = int(box.id.tolist()[0])
            bbox = box.xyxy.tolist()[0]
            object_class_id = box.cls.tolist()[0]
            object_class_name = name_dict[object_class_id]

            if object_class_name in ['car', 'truck', 'motorcycle', 'bus']:
                detected_objects[track_id] = bbox

        return detected_objects

    def draw_annotations(self, frames, object_detections):
        output_video_frames = []
        color_dict = {
            'bicycle': (0, 255, 0),  # Green
            'car': (255, 0, 0),  # Blue
            'motorcycle': (0, 0, 255),  # Red
            'bus': (255, 255, 0),  # Cyan
            'truck': (0, 255, 255),  # Yellow
        }

        counter = 0
        track_ids = []

        for frame, detections in zip(frames, object_detections):
            for track_id, bbox in detections.items():
                x1, y1, x2, y2 = bbox

                object_color = color_dict.get("car", (random.randint(0,255), random.randint(0,255), random.randint(0,255)))

                # Calculate center point
                cx = int(x1 + x2) // 2
                cy = int(y1 + y2) // 2

                cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)
                cv2.line(frame, (450, 1100), (2100, 1100), (255, 255, 255), 1)

                # Vehicle label
                label = f"Car {track_id}"
                cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, object_color, 2)

                # Count vehicles that cross the line
                if cy > 1100:  # crossing line y position
                    if track_id not in track_ids:
                        track_ids.append(track_id)
                        counter += 1

                # Draw bounding box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), object_color, 2)

            # Display total vehicle count
            cv2.putText(frame, f"Vehicles Count: {counter}", (2100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            output_video_frames.append(frame)

        return output_video_frames
