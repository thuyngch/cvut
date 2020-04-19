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
		cv2.rectange(image_, (x1,y1), (x2,y2), color, thickness=thickness)
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
