import os
import cv2
from time import time, sleep
from threading import Thread, Lock


__all__ = ["setup_cv2_window", "get_video", "create_video",
           "StreamVideoCapture"]


# ------------------------------------------------------------------------------
#  Utils
# ------------------------------------------------------------------------------
def setup_cv2_window(winname, focus=True, loc=None):
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    if loc is not None:
        cv2.moveWindow(winname, *loc)
    if focus:
        cv2.setWindowProperty(
            winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty(
            winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)


def get_video(video_file):
    cap = cv2.VideoCapture(video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    return cap, (width, height), num_frames, fps


def create_video(out_file, out_size, fps=30):
    dirname = os.path.dirname(out_file)
    os.makedirs(dirname, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(out_file, fourcc, fps, out_size)
    return out


class StreamVideoCapture(object):
    """Realtime RTSP stream, dealing with latency"""
    lock = Lock()
    last_ready = False

    def __init__(self, cap_or_link_or_path, sleep_time=0, num_runs_get_fps=-1):
        self.sleep_time = sleep_time

        # video capture
        if isinstance(cap_or_link_or_path, str):
            self.cap = cv2.VideoCapture(cap_or_link_or_path)
        else:
            self.cap = cap_or_link_or_path

        # measure fps
        if num_runs_get_fps != -1:
            fps = self._get_fps(num_runs_get_fps)
            print("Stream FPS:", fps)
            self.sleep_time = 1 / fps

        # run thread
        thread = Thread(target=self._run)
        thread.daemon = True
        thread.start()
        sleep(1)

    def read(self):
        if self.last_ready:
            status, frame = self.cap.retrieve()
            return status, frame
        else:
            return False, None

    def _run(self):
        while True:
            with self.lock:
                self.last_ready = self.cap.grab()
            sleep(self.sleep_time)

    def _get_fps(self, num_runs=100):
        print("Measuring stream...")
        tic = time()
        for _ in range(num_runs):
            self.cap.grab()
        runtime = time() - tic
        fps = num_runs / runtime
        return fps
