import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

__all__ = ['RoIFilter']


# ------------------------------------------------------------------------------
#   RoIFilter
# ------------------------------------------------------------------------------
class RoIFilter(object):

    MODES = ['center', 'bottom_center', 'top_center']

    def __init__(self, roi):
        if isinstance(roi, list):
            self.roi = Polygon([
                tuple(item)
                for item in np.array(roi).reshape(-1, 2).tolist()])
        elif isinstance(roi, np.ndarray):
            self.roi = Polygon([
                tuple(item)
                for item in roi.reshape(-1, 2).tolist()])

    def __call__(self, bboxes, mode='bottom_center'):
        """Check whether bboxes in RoI"""
        assert mode in self.MODES
        points = [self._get_point(x1, y1, x2, y2, mode)
                  for (x1, y1, x2, y2) in bboxes[:, :4]]
        points = [Point(x, y) for (x, y) in points]

        inroi_inds = []
        for point in points:
            if self.roi.contains(point):
                inroi_inds.append(True)
            else:
                inroi_inds.append(False)
        return np.array(inroi_inds)

    def _get_point(self, x1, y1, x2, y2, mode):
        if mode == 'center':
            x = 0.5 * (x1 + x2)
            y = 0.5 * (y1 + y2)
        elif mode == 'bottom_center':
            x = 0.5 * (x1 + x2)
            y = y2
        elif mode == 'top_center':
            x = 0.5 * (x1 + x2)
            y = y1
        return x, y
