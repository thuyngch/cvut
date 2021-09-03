import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

__all__ = ['RoIFilter']


# ------------------------------------------------------------------------------
#   RoIFilter
# ------------------------------------------------------------------------------
class RoIFilter(object):

    MODES = ['center', 'bottom_center', 'top_center', 'intersect']

    def __init__(self, roi, mode, intersect_thr=0.1):
        assert mode in self.MODES
        self.mode = mode
        self.intersect_thr = intersect_thr

        if isinstance(roi, list):
            self.roi = Polygon([
                tuple(item)
                for item in np.array(roi).reshape(-1, 2).tolist()])
        elif isinstance(roi, np.ndarray):
            self.roi = Polygon([
                tuple(item)
                for item in roi.reshape(-1, 2).tolist()])

    def __call__(self, bboxes):
        """Check whether bboxes in RoI"""
        if self.mode != 'intersect':
            points = [self._get_point(x1, y1, x2, y2, self.mode)
                      for (x1, y1, x2, y2) in bboxes[:, :4]]
            points = [Point(x, y) for (x, y) in points]

            inroi_inds = []
            for point in points:
                inroi_inds.append(self.roi.contains(point))
        else:
            query_polygons = [Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
                              for (x1, y1, x2, y2) in bboxes[:, :4]]
            intersect_ratios = [self._compute_intersect(query_polygon, self.roi)
                                for query_polygon in query_polygons]
            inroi_inds = [ratio >= self.intersect_thr
                          for ratio in intersect_ratios]
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
        else:
            raise NotImplementedError
        return x, y

    def _compute_intersect(self, p1, p2):
        ratio = p1.intersection(p2).area / p1.area
        return ratio


# ------------------------------------------------------------------------------
#  Test bench
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    import time

    def test_itersect_ratio():
        roi = [(0, 0), (1000, 0), (1000, 1000), (0, 1000)]
        query = [(0, 0), (100, 0), (100, 100), (0, 100)]

        roi_filter = RoIFilter(roi, mode='intersect', intersect_thr=0.1)
        ratio = roi_filter._compute_intersect(Polygon(query), Polygon(roi))
        assert ratio == 1

    num_runs = 100
    tic = time.perf_counter()
    for _ in range(num_runs):
        test_itersect_ratio()
    toc = time.perf_counter()
    print("test_itersect_ratio: avg. time {} ms".format(
        int(1e3 * (toc - tic) / num_runs)))
