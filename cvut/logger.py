#------------------------------------------------------------------------------
#   Libraries
#------------------------------------------------------------------------------
import os, cv2, logging
from time import gmtime, strftime
from logging.handlers import TimedRotatingFileHandler


#------------------------------------------------------------------------------
#   Logger
#------------------------------------------------------------------------------
class Logger(logging.Logger):
	def __init__(self, logname, logdir=None, when='D', backupCount=7*5*12):
		# Workdir
		self.logname = logname
		self.logdir = logdir
		if logdir is not None:
			os.makedirs(logdir, exist_ok=True)

		# Error
		self.error_id = 0

		# Create logger
		formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(lineno)d: %(message)s")

		if logdir is not None:
			logfile = os.path.join(logdir, "%s.log" % (logname))
			filehandler = TimedRotatingFileHandler(logfile, when=when, backupCount=backupCount)
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
			self.info("Logger \'{}\' will be written at {}".format(self.logname, logfile))

	def log_error(self, image):
		self.error_id += 1
		filename = "%d-%s.jpg" % (self.error_id, strftime("%Y-%m-%d-%H:%M:%S", gmtime()))
		image_file = self.save_image(image, cate='error', filename=filename)
		self.info("Image yielding the Error-%d is saved at %s" % (self.error_id, image_file))

	def save_image(self, image, cate=None, filename=None):
		if cate is not None:
			folder = os.path.join(self.logdir, cate)
			os.makedirs(folder, exist_ok=True)
		else:
			folder = self.logdir

		if filename is not None:
			image_file = os.path.join(folder, filename)
		else:
			image_file = os.path.join(folder, "%s.jpg" % (strftime("%Y-%m-%d-%H:%M:%S", gmtime())))

		cv2.imwrite(image_file, image[...,::-1])
		return image_file
