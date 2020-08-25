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
	_color_random = np.random.randint(0, 256, (3,), dtype='uint8')
	COLOR_DICT[i] = tuple(_color_random.tolist())
COLOR_LEN = len(COLOR_DICT)


#------------------------------------------------------------------------------
#  draw_bboxes
#------------------------------------------------------------------------------
def draw_bboxes(image, bboxes, labels=None, classnames=None, color=(0,255,0),
			thickness=1, font=_FONT, font_size=0.5, font_thickness=2):
	"""
	image (np.uint8) shape [H,W,3], RGB image
	bboxes (np.int/np.float/list) shape [N,4], format [x1, y1, x2, y2]
	labels (np.int/list) shape [N,], start-from-0
	classnames (list) of string, len [N,]
	"""
	image_ = image.copy()
	if labels is None:
		for bbox in bboxes:
			x1, y1, x2, y2 = [int(ele) for ele in bbox]
			cv2.rectangle(image_, (x1,y1), (x2,y2), color, thickness=thickness)
	else:
		for bbox, label in zip(bboxes, labels):
			color_idx = int(label % COLOR_LEN)
			_color = COLOR_DICT[color_idx] if color is None else color
			x1, y1, x2, y2 = [int(ele) for ele in bbox]
			cv2.rectangle(image_, (x1,y1), (x2,y2), _color, thickness=thickness)
			if classnames is not None:
				cv2.putText(
					image_, classnames[label], (x1,y1-2),
					font, font_size, _color, thickness=font_thickness)
	return image_


#------------------------------------------------------------------------------
#  draw_polygons
#------------------------------------------------------------------------------
def draw_polygons(image, polygons, color=(0,255,0), thickness=1):
	"""
	image (np.uint8) shape [H,W,3], RGB image
	polygons (list) of polygon shape [N,2], format [x, y]
	"""
	image_ = image.copy()
	for idx, polygon in enumerate(polygons):
		color_idx = int(idx % COLOR_LEN)
		_color = COLOR_DICT[color_idx] if color is None else color
		polygon = polygon.astype(int).reshape((-1,1,2))
		cv2.polylines(image_, [polygon], True, _color, thickness=thickness)
	return image_


#------------------------------------------------------------------------------
#  draw_inst_masks
#------------------------------------------------------------------------------
def draw_inst_masks(image, masks, color=None):
	"""
	image (np.uint8) shape [H,W,3], RGB image
	masks (np.int/np.uint8/np.bool) shape [N,H,W], value in {0;1}
	"""
	image_ = image.copy()

	for idx, mask in enumerate(masks):
		if color is not None:
			color_mask = np.array(color)
		else:
			color_mask = np.array(COLOR_DICT[idx])

		image_[mask==1] = image_[mask==1] * 0.5 + color_mask * 0.5

	return image_


#------------------------------------------------------------------------------
#  draw_masks_overlay
#------------------------------------------------------------------------------
def draw_masks_overlay(image, masks, color=None, alpha=0.5):
	"""
	image (np.uint8) shape [H,W,3], RGB image
	masks (np.int/np.uint8/np.bool/np.float) shape [N,H,W], value in range [0;1]
	"""
	image_ = image.copy()

	np.random.seed(0)
	if color is not None:
		color_masks = [np.array(color)] * len(masks)
	else:
		color_masks = [
			np.random.randint(0, 256, (3,), dtype='uint8')
			for _ in range(len(masks))]

	for mask, color_mask in zip(masks, color_masks):
		mask_overlay = (mask[...,None] * color_mask[None,None,...])
		mask_overlay = mask_overlay.astype('uint8')
		image_[mask==1,...] = alpha * image[mask==1,...] + \
			(1-alpha) * mask_overlay[mask==1,...]

	return image_


#------------------------------------------------------------------------------
#  draw_track
#------------------------------------------------------------------------------
def draw_track(image, bboxes, ids, labels=None, classnames=None,
	       masks=None, polygons=None, thickness=1,
	       font=_FONT, font_size=0.5, font_thickness=1):
	"""
	image (np.uint8) shape [H,W,3], RGB image
	bboxes (np.int/np.float/list) shape [N,4], format [x1, y1, x2, y2]
	ids (np.int/np.float/list) shape [N]
	labels (np.int/list) shape [N,], start-from-0. None is not used.
	classnames (list) of string, len [N,]. None is not used.
	masks (np.int/np.float/list) [N, H, W]
	polygons (list) list of [K, 2]
	"""
	image_ = image.copy()
	assert len(bboxes) == len(ids), \
		"len(bboxes)={} vs. len(ids)={}".format(len(bboxes), len(ids))

	if labels is None:
		for bbox, track_id in zip(bboxes, ids):
			x1, y1, x2, y2 = [int(ele) for ele in bbox]
			_color = COLOR_DICT[track_id % len(COLOR_DICT)]
			cv2.rectangle(image_, (x1,y1), (x2,y2), _color, thickness=thickness)
			cv2.putText(image_, "ID{}".format(track_id),
				(int((x1+x2)/2), int((y1+y2)/2)),
				font, font_size, _color, thickness=font_thickness)
	else:
		for bbox, track_id, label in zip(bboxes, ids, labels):
			x1, y1, x2, y2 = [int(ele) for ele in bbox]
			_color = COLOR_DICT[track_id % len(COLOR_DICT)]
			cv2.rectangle(image_, (x1,y1), (x2,y2), _color, thickness=thickness)
			text = "cls{}-ID{}".format(label, track_id) if classnames is None \
				else "{}-ID{}".format(classnames[label], track_id)
			cv2.putText(
				image_, text, (int((x1+x2)/2), int((y1+y2)/2)),
				font, font_size, _color, thickness=font_thickness)

	if masks is not None:
		for track_id, mask in zip(ids, masks):
			_color = COLOR_DICT[track_id % len(COLOR_DICT)]
			image_ = draw_masks_overlay(
				image_, np.expand_dims(mask, axis=0), color=_color)

	if polygons is not None:
		for track_id, polygon in zip(ids, polygons):
			_color = COLOR_DICT[track_id % len(COLOR_DICT)]
			image_ = draw_polygons(
				image_, [polygon], color=_color, thickness=thickness)

	return image_


#------------------------------------------------------------------------------
#  draw_keypoints
#------------------------------------------------------------------------------
def draw_keypoints(image, points_list, ids=None,
				scale=1.0, radius=1, color=(0,255,0),
				put_text=False, font=_FONT, font_size=0.5, font_thickness=1):
	"""
	image (np.uint8) shape [H,W,3], RGB image
	points_list (list) shape [num_points,3] format [x,y,visible]/[num_points,2]
	"""
	image_ = image.copy()
	for idx in range(len(points_list)):

		if ids is not None:
			color_idx = int(ids[idx] % COLOR_LEN)
		else:
			color_idx = int(idx % COLOR_LEN)
		_color = COLOR_DICT[color_idx] if color is None else color

		points = points_list[idx]
		for point_id, point in enumerate(points):

			if len(point) == 3:
				x, y, visible = [int(scale * ele) for ele in point]
			else:
				x, y = [int(scale * ele) for ele in point]
				visible = 1

			if visible!=0:
				image_ = cv2.circle(image_, (x,y), radius, _color, -1)
				if put_text:
					image_ = cv2.putText(image_, str(point_id+1),
						(x,y), font, font_size, _color, font_thickness)
	return image_
