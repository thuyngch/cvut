import os
import cv2


__all__ = ["setup_cv2_window", "create_video"]


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


def create_video(out_file, out_size, fps=30):
    dirname = os.path.dirname(out_file)
    os.makedirs(dirname, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(out_file, fourcc, fps, out_size)
    return out
