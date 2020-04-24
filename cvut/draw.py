#------------------------------------------------------------------------------
#  Libraries
#------------------------------------------------------------------------------
import cv2, mmcv
import numpy as np


#------------------------------------------------------------------------------
#  draw_bboxes
#------------------------------------------------------------------------------
def draw_bboxes(image, bboxes, color=(0,255,0), thickness=1):
	"""
	image (np.uint8) of shape [H,W,3], RGB image
	bboxes (np.int/np.float/list) of shape [N,4], format [x1, y1, x2, y2]
	"""
	image_ = image.copy()
	for bbox in bboxes:
		x1, y1, x2, y2 = [int(ele) for ele in bbox]
		cv2.rectangle(image_, (x1,y1), (x2,y2), color, thickness=thickness)
	return image_


#------------------------------------------------------------------------------
#  draw_polygons
#------------------------------------------------------------------------------
def draw_polygons(image, polygons, color=(0,255,0), thickness=1):
	"""
	image (np.uint8) of shape [H,W,3], RGB image
	bboxes (np.int/np.float/list) of shape [N,2], format [x, y]
	"""
	image_ = image.copy()
	if isinstance(polygons, list):
		polygons = np.array(polygons).astype(int).reshape((-1,1,2))
	else:
		polygons = polygons.astype(int).reshape((-1,1,2))
	cv.polylines(image_, [polygons], True, color, thickness=thickness)
	return image_


#------------------------------------------------------------------------------
#  draw_inst_masks
#------------------------------------------------------------------------------
def draw_inst_masks(image, masks):
	"""
	image (np.uint8) of shape [H,W,3], RGB image
	masks (np.int/np.uint8/np.bool) of shape [N,H,W], value in {0;1}
	"""
	image_ = image.copy()

	np.random.seed(42)
	color_masks = [
		np.random.randint(0, 256, (1, 3), dtype='uint8')
		for _ in range(len(masks))]

	for mask, color_mask in zip(masks, color_masks):
		image_[mask==1] = image_[mask==1] * 0.5 + color_mask * 0.5

	return image_
