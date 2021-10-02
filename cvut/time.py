import time
from datetime import datetime

__all__ = ["TIME_FMT_SEC", "TIME_FMT_DATE", "TIME_FMT_MIC",
           "TIME_FMT_SEC_TZ", "TIME_FMT_DATE_TZ", "TIME_FMT_MIC_TZ",
           "get_time_now", "str2time", "time2str", "Timer"]


# ------------------------------------------------------------------------------
#  Utils
# ------------------------------------------------------------------------------
TIME_FMT_SEC = "%Y-%m-%d-%H-%M-%S"
TIME_FMT_DATE = "%Y-%m-%d"
TIME_FMT_MIC = "%Y-%m-%d-%H-%M-%S-%f"
TIME_FMT_SEC_TZ = "%Y-%m-%d-%H-%M-%S-%Z"
TIME_FMT_DATE_TZ = "%Y-%m-%d-%Z"
TIME_FMT_MIC_TZ = "%Y-%m-%d-%H-%M-%S-%f-%Z"


def get_time_now(fmt=TIME_FMT_SEC, to_str=True):
    cur_time = datetime.now()
    if to_str:
        cur_time = cur_time.strftime(fmt)
    return cur_time


def str2time(str_time, fmt=TIME_FMT_SEC):
    return datetime.strptime(str_time, fmt)


def time2str(time_obj, fmt=TIME_FMT_SEC):
    return time_obj.strftime(fmt)


# ------------------------------------------------------------------------------
#  Timer
# ------------------------------------------------------------------------------
class Timer(object):

    def __init__(self):
        self.total_time = 0.
        self.calls = 0
        self.start_time = 0.
        self.diff = 0.
        self.average_time = 0.

    def tic(self):
        # using time.time instead of time.clock because time time.clock
        # does not normalize for multithreading
        self.start_time = time.time()

    def toc(self, average=True):
        self.diff = time.time() - self.start_time
        self.total_time += self.diff
        self.calls += 1
        self.average_time = self.total_time / self.calls
        if average:
            return self.average_time
        else:
            return self.diff

    def clear(self):
        self.total_time = 0.
        self.calls = 0
        self.start_time = 0.
        self.diff = 0.
        self.average_time = 0.
