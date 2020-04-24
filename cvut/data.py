#------------------------------------------------------------------------------
#  Libraries
#------------------------------------------------------------------------------
import base64
import numpy as np
import pycocotools.mask as mask_util


#------------------------------------------------------------------------------
#  FIFOQueue
#------------------------------------------------------------------------------
class FIFOQueue(object):
	def __init__(self, queue_len):
		self.queue = queue_len * [None]
		self.queue_len = queue_len

	def push(self, item):
		overflow_item = None
		if len(self.queue)==self.queue_len:
			overflow_item = self.pop()

		self.queue.append(item)
		return overflow_item

	def pop(self):
		item = self.queue.pop(0)
		return item

	def check_in_queue(self, item):
		return item in self.queue

	def check_unique_item(self):
		uniq_item = self.queue[0]
		for item in self.queue[1:]:
			if item!=uniq_item:
				return False
		return True

	def reset(self):
		self.queue = self.queue_len * [None]

	def __str__(self):
		return "[{}] {}".format(self.__class__.__name__, self.queue)


#------------------------------------------------------------------------------
#  Base64 encode/decode
#------------------------------------------------------------------------------
def encode_base64(image):
	image_base64 = base64.b64encode(image.copy(order='C')).decode("utf-8")
	return image_base64

def decode_base64(base64_code, shape, dtype='uint8'):
	base64_code = bytes(base64_code, encoding="utf-8")
	image = np.frombuffer(base64.decodebytes(base64_code), dtype=dtype)
	image = image.reshape(shape)
	return image


#------------------------------------------------------------------------------
#  RLE encode/decode
#------------------------------------------------------------------------------
def encode_rle(bin_mask):
	rle = mask_util.encode(np.array(bin_mask[:, :, np.newaxis], order='F'))[0]
	return rle

def decode_rle(rle):
	bin_mask = mask_util.decode(rle)
	return bin_mask


# #------------------------------------------------------------------------------
# #  Test bench for encode base64
# #------------------------------------------------------------------------------
# if __name__ == "__main__":
# 	import cv2
# 	from time import time

# 	image_file = "/home/piflab/thuync/dataset/video/extracted_day5/side_fish_1/frame_5341.jpg"
# 	image = cv2.imread(image_file)

# 	tic = time()
# 	image_base64 = encode_base64(image)
# 	encode_time = time() - tic

# 	tic = time()
# 	image_recons = decode_base64(image_base64, image.shape)
# 	decode_time = time() - tic

# 	err = np.abs(image - image_recons).mean()
# 	print("Error: {}; Shape: {}; encode_len: {} [kB]; encode_time: {} [ms]; decode_time: {} [ms]".format(
# 		err, image.shape, len(image_base64)/1024, int(1000*encode_time), int(1000*decode_time)))


#------------------------------------------------------------------------------
#  Test bench for encode rle
#------------------------------------------------------------------------------
if __name__ == "__main__":
	import cv2
	from time import time

	image_file = "/home/piflab/thuync/dataset/video/extracted_day5/side_fish_1/frame_5341.jpg"
	image = cv2.imread(image_file)
	bin_mask = (image[...,0] > 127).astype('uint8')

	tic = time()
	rle = encode_rle(bin_mask)
	encode_time = time() - tic

	tic = time()
	bin_mask_recons = decode_rle(rle)
	decode_time = time() - tic

	err = np.abs(bin_mask - bin_mask_recons).mean()
	print("Error: {}; Shape: {}; encode_len: {} [kB]; encode_time: {} [ms]; decode_time: {} [ms]".format(
		err, bin_mask.shape, int(len(rle['counts'])/1024), int(1000*encode_time), int(1000*decode_time)))
