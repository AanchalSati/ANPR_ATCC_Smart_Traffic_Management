import ast
import cv2
import numpy as np
import pandas as pd
import re

# Load CSV
results = pd.read_csv('output/interpolated_main.csv')

# Load video
video_path = 'data/traffic.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Video properties: FPS={fps}, Width={width}, Height={height}")

out = cv2.VideoWriter('output_video/output.mp4', fourcc, fps, (width, height))

# Preprocess license plate information
license_plate = {}

for car_id in np.unique(results['car_id']):
    max_score = np.amax(results[results['car_id'] == car_id]['license_number_score'])
    license_plate[car_id] = {
        'car_class': results[
            (results['car_id'] == car_id) & (results['license_number_score'] == max_score)
        ]['car_class'].iloc[0],
        'license_plate_number': results[
            (results['car_id'] == car_id) & (results['license_number_score'] == max_score)
        ]['license_number'].iloc[0]
    }

# Function to parse bbox strings
def parse_bbox(bbox_str):
    try:
        # Check if the string is a properly formatted list
        if '[' in bbox_str and ']' in bbox_str:
            return ast.literal_eval(bbox_str)
        # Otherwise, assume it is space-separated float values
        return list(map(float, bbox_str.split()))
    except Exception as e:
        print(f"Error parsing bbox: {bbox_str} -> {e}")
        return None

frame_nmr = -1
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Read frames
ret = True
while ret:
    ret, frame = cap.read()
    frame_nmr += 1
    if not ret:
        break

    df_ = results[results['frame_nmr'] == frame_nmr]
    for row_indx in range(len(df_)):
        try:
            # Parse car bounding box
            car_bbox_str = df_.iloc[row_indx]['car_bbox']
            car_bbox = parse_bbox(car_bbox_str)
            if car_bbox is None or len(car_bbox) != 4:
                print(f"Invalid car_bbox format in row {row_indx}: {car_bbox_str}")
                continue
            car_x1, car_y1, car_x2, car_y2 = car_bbox

            # Parse license plate bounding box
            license_plate_bbox_str = df_.iloc[row_indx]['license_plate_bbox']
            license_plate_bbox = parse_bbox(license_plate_bbox_str)
            if license_plate_bbox is None or len(license_plate_bbox) != 4:
                print(f"Invalid license_plate_bbox format in row {row_indx}: {license_plate_bbox_str}")
                continue
            x1, y1, x2, y2 = license_plate_bbox

            # Determine object color based on car class
            color_dict = {
                "car": (0, 255, 0),
                "bus": (0, 0, 255),
                "truck": (255, 0, 0),
                "motorcycle": (255, 255, 0),
                "0": (0, 255, 255)
            }
            object_class_name = license_plate[df_.iloc[row_indx]['car_id']]['car_class']
            object_color = color_dict.get(object_class_name, (255, 255, 255))  # Default to white

            # Draw car bounding box
            cv2.rectangle(frame, (int(car_x1), int(car_y1)), (int(car_x2), int(car_y2)), object_color, 2)

            # Draw license plate bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)

            # Add text for license plate
            cv2.putText(
                frame,
                f"{object_class_name}: {license_plate[df_.iloc[row_indx]['car_id']]['license_plate_number']}",
                (int(car_x1), int(car_y1) - 10),  # Position text slightly above the car box
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                object_color,
                2
            )
        except Exception as e:
            print(f"Error processing row {row_indx}: {e}")
            continue

    # Write frame to output video
    out.write(frame)

out.release()
cap.release()
print("Video processing completed!")

