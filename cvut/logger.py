# ------------------------------------------------------------------------------
#   Libraries
# ------------------------------------------------------------------------------
import os
import cv2
import logging
import numpy as np
from logging.handlers import TimedRotatingFileHandler

from .time import get_time_now

__all__ = ["Logger"]


# ------------------------------------------------------------------------------
#   Logger
# ------------------------------------------------------------------------------
class Logger(logging.Logger):
    def __init__(self, logname, logdir=None, when='H', backupCount=24*7):
        # Workdir
        self.logname = logname
        self.logdir = logdir
        if logdir is not None:
            os.makedirs(logdir, exist_ok=True)

        # Error
        self.error_id = 0

        # Create logger
        formatter = logging.Formatter(
            "%(asctime)s-%(levelname)s-%(name)s-%(filename)s-%(lineno)d: %(message)s")

        if logdir is not None:
            logfile = os.path.join(logdir, "%s.log" % (logname))
            filehandler = TimedRotatingFileHandler(
                logfile, when=when, backupCount=backupCount)
            filehandler.suffix = "%Y%m%d%H"
            filehandler.setLevel(logging.INFO)
            filehandler.setFormatter(formatter)

        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        streamhandler.setFormatter(formatter)

        super(Logger, self).__init__(logname)
        self.setLevel(logging.INFO)
        if logdir is not None:
            self.addHandler(filehandler)
        self.addHandler(streamhandler)
        if logdir is not None:
            self.info("Logger \'{}\' will be written at {}".format(
                self.logname, logfile))

    def log_error(self, img):
        self.error_id += 1
        filename = "{}-{}.jpg".format(self.error_id, get_time_now())
        img_file = self.save_img(img, cate='error', filename=filename)
        self.info("Image yielding the Error-%d is saved at %s" %
                  (self.error_id, img_file))

    def save_img(self, img, embed=None, cate=None, sub_cate=None,
                 filename=None, sep_date=False):
        # get folder
        if cate is not None:
            folder = os.path.join(self.logdir, cate)
            if sep_date:
                folder = os.path.join(folder, get_time_now("%Y-%m-%d"))
            if sub_cate is not None:
                folder = os.path.join(folder, sub_cate)
            os.makedirs(folder, exist_ok=True)
        else:
            folder = self.logdir

        # get img_file
        if filename is not None:
            img_file = os.path.join(folder, filename)
        else:
            img_file = os.path.join(folder, "{}.jpg".format(get_time_now()))

        # save img and embed
        cv2.imwrite(img_file, img)
        if embed is not None:
            embed_file = img_file.replace('.jpg', '.npy')
            np.save(embed_file, embed)

        return img_file
