from ultralytics import YOLO
import cv2

class Tracker:

    def __init__(self):
        self.model = YOLO("yolov8x.pt")

    def process_video(self, frames):
        detections = []
        output_video_frames = []
        
        color_dict = { 
            "car": (0,255,0), 
            "bus": (0,0,255), 
            "truck": (255,0,0), 
            "motorcycle": (255,255,0), 
            "bicycle": (0,255,255) 
        }

        cy1 = 1100
        offset = 6

        counter = 0
        track_ids = []
        
        valid_classes = ["car", "bus", "truck", "motorcycle", "bicycle"]
        
        for frame in frames:
            results = self.model.track(frame, persist=True)[0]
            name_dict = results.names
            
            frame_detections = {}
            
            for box in results.boxes:
                track_id = int(box.id.tolist()[0])
                result = box.xyxy.tolist()[0]
                object_class_id = box.cls.tolist()[0]
                object_class_name = name_dict[object_class_id]
                
                if object_class_name in valid_classes:
                    frame_detections[track_id] = {object_class_name: result}
                    
                    object_color = color_dict[object_class_name]
                    x1, y1, x2, y2 = result
                    label = f"{object_class_name} {track_id}"

                    cx = int(x1 + x2) // 2
                    cy = int(y1 + y2) // 2 

                    cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

                    #
                    cv2.line(frame, (450, 1100), (2100, 1100), (255, 255, 255), 1)
                    
                    cv2.putText(frame, label, (int(x1), int(y1 - 10)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, object_color, 2)
                    cv2.rectangle(frame, (int(x1), int(y1)),(int(x2), int(y2)), object_color, 2)

                    if cy1<cy:

                        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

                        if track_id not in track_ids:
                            track_ids.append(track_id)
                            counter += 1



            
            detections.append(frame_detections)
            output_video_frames.append(frame)
        
        return output_video_frames



















