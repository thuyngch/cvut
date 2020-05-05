#------------------------------------------------------------------------------
#  Libraries
#------------------------------------------------------------------------------
import cv2, mmcv
import numpy as np


#------------------------------------------------------------------------------
#  Constants
#------------------------------------------------------------------------------
_FONT = cv2.FONT_HERSHEY_SIMPLEX

np.random.seed(0)
COLOR_DICT = dict()
for i in range(256):
	color = np.random.randint(0, 256, (3,), dtype='uint8')
	COLOR_DICT[i] = tuple(color.tolist())


#------------------------------------------------------------------------------
#  draw_bboxes
#------------------------------------------------------------------------------
def draw_bboxes(image, bboxes, labels=None, classnames=None, color=(0,255,0),
			thickness=1, font=_FONT, font_size=0.5, text_thickness=2):
	"""
	image (np.uint8) of shape [H,W,3], RGB image
	bboxes (np.int/np.float/list) of shape [N,4], format [x1, y1, x2, y2]
	labels (np.int/list) of shape [N,], start-from-0
	classnames (list) of string, len [N,]
	"""
	image_ = image.copy()
	if labels is None:
		for bbox in bboxes:
			x1, y1, x2, y2 = [int(ele) for ele in bbox]
			cv2.rectangle(image_, (x1,y1), (x2,y2), color, thickness=thickness)
	else:
		for bbox, label in zip(bboxes, labels):
			color = COLOR_DICT[label % len(COLOR_DICT)] if color is None else color
			x1, y1, x2, y2 = [int(ele) for ele in bbox]
			cv2.rectangle(image_, (x1,y1), (x2,y2), color, thickness=thickness)
			if classnames is not None:
				cv2.putText(
					image_, classnames[label], (x1,y1-2),
					font, font_size, color, thickness=text_thickness)
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


#------------------------------------------------------------------------------
#  draw_track
#------------------------------------------------------------------------------
def draw_track(image, bboxes, ids, thickness=1,
			font=_FONT, font_size=0.5, text_thickness=2):
	"""
	image (np.uint8) of shape [H,W,3], RGB image
	bboxes (np.int/np.float/list) of shape [N,4], format [x1, y1, x2, y2]
	ids (np.int/np.float/list) of shape [N]
	"""
	assert len(bboxes) == len(ids), \
		"len(bboxes)={} vs. len(ids)={}".format(len(bboxes), len(ids))

	image_ = image.copy()
	for bbox, track_id in zip(bboxes, ids):
		x1, y1, x2, y2 = [int(ele) for ele in bbox]
		color = COLOR_DICT[track_id % len(COLOR_DICT)]
		cv2.rectangle(image_, (x1,y1), (x2,y2), color, thickness=thickness)
		cv2.putText(
			image_, "ID{}".format(track_id), (int((x1+x2)/2), int((y1+y2)/2)),
			font, font_size, color, thickness=text_thickness)
	return image_


#------------------------------------------------------------------------------
#  draw_keypoints
#------------------------------------------------------------------------------
def draw_keypoints(image, points_list, scale=1.0, radius=1,
				thickness=1, font=_FONT, font_size=0.5):
	"""
	image (np.uint8) of shape [H,W,3], RGB image
	points_list (list) of shape [num_points,3], format [x,y,visible]
	"""
	image_ = image.copy()
	for points in points_list:
		color = np.random.randint(0, 256, (3,)).tolist()
		for point_id, point in enumerate(points):
			x, y, visible = [int(scale * ele) for ele in point]
			if visible!=0:
				image_ = cv2.circle(image_, (x,y), radius, color, -1)
				image_ = cv2.putText(image_, str(point_id+1),
					(x,y), font, font_size, color, thickness)
	return image_
