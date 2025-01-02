from ultralytics import YOLO
import cv2

import numpy as np

from utils.util import get_car, read_license_plate, write_csv

class Tracker:
    # 2: 'car',
    # 3: 'motorcycle',
    # 5: 'bus',
    # 7: 'truck'
    def __init__(self):
        # load models
        self.vehicle_detection_model = YOLO("yolov8x.pt")
        self.license_plate_detector = YOLO("number_plate_detection_2nd_dec.pt")
        self.results = {}
        self.vehicles = [2, 3, 5, 7]

    def process_video(self, frames):

        for frame_no, frame in enumerate(frames):
            self.results[frame_no] = {}

            detections = self.vehicle_detection_model.track(frame,persist=True)[0]
            # print(f"outer detection\n{detections.boxes.data.tolist()}")
            class_names = detections.names
            detections_ = []

            # for detection in detections.boxes.data.tolist():
            #     x1, y1, x2, y2, track_id, score, class_id = detection
            #     if int(class_id) in self.vehicles:
            #         detections_.append([x1, y1, x2, y2, track_id, class_id])

            for detection in detections.boxes:
                track_id = int(detection.id.tolist()[0])
                x1,y1,x2,y2 = detection.xyxy.tolist()[0]
                obj_class_id = detection.cls.tolist()[0]
                object_class_name = class_names[obj_class_id]

                if int(obj_class_id) in self.vehicles:
                    detections_.append([x1, y1, x2, y2, track_id, object_class_name])


            # detect license plates
            license_plates = self.license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # assign license plate to car
                # xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, detections_)
                xcar1, ycar1, xcar2, ycar2, car_id, car_class = get_car(license_plate, detections_)


                if car_id != -1:

                    # crop license plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                    # process license plate
                    sharpen_kernel = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
                    license_plate_crop_thresh = cv2.filter2D(license_plate_crop, -1, sharpen_kernel)

                    license_plate_crop_thresh = 255 - license_plate_crop_thresh


                    # read license plate number
                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
                    if license_plate_text is not None:
                        self.results[frame_no][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2],
                                                                  'obj_class':car_class},
                                                      'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                        'text': license_plate_text,
                                                                        'bbox_score': score,
                                                                        'text_score': license_plate_text_score}}
            # frame = cv2.resize(frame, (1280, 720))
            # cv2.imshow('frame', frame)
            # if cv2.waitKey(0) & 0xFF == ord('q'):
            #     break
        # write results
        write_csv(self.results, 'output/main.csv')