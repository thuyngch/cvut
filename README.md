# cvut
Computer Vision UTils


## Installation
```bash
pip install git+https://github.com/thuyngch/cvut
```


## Example

- Convert PyTorch tensor (of shape [3, H, W]) to numpy image (of shape [H, W, 3]):
```python
image = cvut.impt2np(img.unsqueeze(0))
mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375]
image = cvut.imdenormalize(image, mean, std, scale_255=False)
```
