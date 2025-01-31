# ------------------------------------------------------------------------------
#   Libraries
# ------------------------------------------------------------------------------
import os
import sys
import time
import json
import logging
import linecache
from logging.handlers import TimedRotatingFileHandler

from .time import get_time_now

__all__ = ["Logger", "basename", "print_dict_beauty"]


# ------------------------------------------------------------------------------
#  Utils
# ------------------------------------------------------------------------------
def basename(filepath, wo_fmt=False):
    bname = os.path.basename(filepath)
    if wo_fmt:
        bname = '.'.join(bname.split('.')[:-1])
    return bname


def print_dict_beauty(dict_data, indent=4):
    print(json.dumps(dict_data, indent=indent))


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime("%Y-%m-%d_%H-%M-%S", timeTuple))
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


# ------------------------------------------------------------------------------
#   Logger
# ------------------------------------------------------------------------------
class Logger(logging.Logger):
    def __init__(self,
                 logname,
                 logdir=None,
                 when='H',
                 backupCount=24*7,
                 with_pid=False):
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
            if with_pid:
                pid = os.getpid()
                logfile = os.path.join(logdir, f"{logname}.{pid}.log")
            else:
                logfile = os.path.join(logdir, f"{logname}.log")
            filehandler = CustomTimedRotatingFileHandler(
                logfile, when=when, backupCount=backupCount)
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

    def _log_exception(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        self.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(
            filename, lineno, line.strip(), exc_obj))

    def error(self, message, detail=False):
        super(Logger, self).error(message)
        if detail:
            self._log_exception()
