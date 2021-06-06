# ------------------------------------------------------------------------------
#  Libraries
# ------------------------------------------------------------------------------
import base64
import numpy as np
import pycocotools.mask as mask_util

__all__ = ['FIFOQueue',
           'encode_base64', 'decode_base64',
           'encode_rle', 'decode_rle']


# ------------------------------------------------------------------------------
#  FIFOQueue
# ------------------------------------------------------------------------------
class FIFOQueue(object):
    def __init__(self, queue_len):
        self.queue = queue_len * [None]
        self.queue_len = queue_len

    def push(self, item):
        overflow_item = None
        if len(self.queue) == self.queue_len:
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
            if item != uniq_item:
                return False
        return True

    @property
    def data(self):
        return [item for item in self.queue if item is not None]

    def reset(self):
        self.queue = self.queue_len * [None]

    def __str__(self):
        return "[{}] {}".format(self.__class__.__name__, self.queue)


# ------------------------------------------------------------------------------
#  Base64 encode/decode
# ------------------------------------------------------------------------------
def encode_base64(image):
    image_base64 = base64.b64encode(image.copy(order='C')).decode("utf-8")
    return image_base64


def decode_base64(base64_code, shape, dtype='uint8'):
    base64_code = bytes(base64_code, encoding="utf-8")
    image = np.frombuffer(base64.decodebytes(base64_code), dtype=dtype)
    image = image.reshape(shape)
    return image


# ------------------------------------------------------------------------------
#  RLE encode/decode
# ------------------------------------------------------------------------------
def encode_rle(bin_mask):
    rle = mask_util.encode(np.array(bin_mask[:, :, np.newaxis], order='F'))[0]
    return rle


def decode_rle(rle):
    bin_mask = mask_util.decode(rle)
    return bin_mask
