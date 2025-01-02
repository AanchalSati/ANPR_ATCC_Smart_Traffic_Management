from utils.video_utils import read_video, save_video, detect_vehicles
from object_tracker.tracker import Tracker

def main():

    frames = read_video("data/traffic.mp4")

    #object tracking
    obj_tracker = Tracker()
    # result = obj_tracker.detect_objects(frames)

    # output_frames = obj_tracker.draw_annotations(frames, result)
    output_frames = obj_tracker.process_video(frames)


    save_video(output_frames, "output_video/output_1.avi")

if __name__ == '__main__':
    main()
