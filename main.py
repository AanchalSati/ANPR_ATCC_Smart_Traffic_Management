from utils.video_utils import read_video, save_video
from object_tracker.tracker import Tracker

def main():
    video_path = "C:/Users/anchal/Desktop/SmartTrafficManagement/DATA/traffic_3.mp4"
    frames = read_video(video_path)
    obj_tracker = Tracker()

    detections = obj_tracker.detect_objects(frames)
    output_frames = obj_tracker.draw_annotations(frames, detections)

    save_video(output_frames, "output/traffic_output.avi")

if __name__ == '__main__':
    main()
