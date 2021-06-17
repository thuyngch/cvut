import time
from datetime import datetime

__all__ = ["TIME_FMT", "get_time_now", "str2time", "Timer"]


# ------------------------------------------------------------------------------
#  Utils
# ------------------------------------------------------------------------------
TIME_FMT = "%Y-%m-%d-%H-%M-%S"


def get_time_now(fmt=TIME_FMT, to_str=True):
    cur_time = datetime.now()
    if to_str:
        cur_time = cur_time.strftime(fmt)
    return cur_time


def str2time(str_time, fmt=TIME_FMT):
    return datetime.strptime(str_time, fmt)


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
