# cvut
Computer Vision UTils


## Installation
```bash
pip install git+https://github.com/thuyngch/cvut
```


## Example


#### 1. Image conversion:

* Convert PyTorch tensor `img` (of shape [3, H, W]) to numpy `image` (of shape [H, W, 3]):
```python
image = cvut.impt2np(img.unsqueeze(0))
mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375]
image = cvut.imdenormalize(image, mean, std, scale_255=False)
```


#### 2. Visualization:

* Draw `bboxes` (of shape [N, 5], 5 includes [x1, y1, x2, y2, score]), `labels` (of shape [N]), and `classnames` (list of len [N]):
```python
# fix color for all boxes
image = cvut.draw_bboxes(image, bboxes[:,:4], color=(0,255,0))

# each box has a color
image = cvut.draw_bboxes(image, bboxes[:,:4], color=None)

# boxes sharing the same label have the same color
image = cvut.draw_bboxes(image, bboxes[:,:4], labels, color=None)

# also draw classname texts
image = cvut.draw_bboxes(image, bboxes[:,:4], labels, classnames, color=None)
```
