from utils.video_utils import read_video, save_video, detect_vehicles
from object_tracker.tracker_3 import Tracker

def main():
    frames = read_video("data/traffic.mp4")

    track = Tracker()
    result = track.process_video(frames)

if __name__ == '__main__':
    main()
