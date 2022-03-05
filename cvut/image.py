import os
import mmcv
import numpy as np
from glob import glob


__all__ = ["impt2np", "imdenormalize", "imwrite",
           "glob_imgs", "glob_folders", "glob_files"]

SUPPORT_IMG_FORMATS = ['jpg', 'jpeg', 'png']


# ------------------------------------------------------------------------------
#  impt2np
# ------------------------------------------------------------------------------
def impt2np(image):
    image = image[0].cpu().numpy().transpose((1, 2, 0))
    return image


# ------------------------------------------------------------------------------
#  imdenormalize
# ------------------------------------------------------------------------------
def imdenormalize(image,
                  mean=[123.675, 116.28, 103.53],
                  std=[58.395, 57.12, 57.375],
                  scale_255=False):
    if scale_255:
        image = np.clip(((image * std + mean) * 255.), 0, 255).astype('uint8')
    else:
        image = np.clip(image * std + mean, 0, 255).astype('uint8')
    return image


# ------------------------------------------------------------------------------
#  imwrite
# ------------------------------------------------------------------------------
def imwrite(image, outfile):
    mmcv.imwrite(image, outfile)
    print("[cvut] Image is saved at {}".format(outfile))


# ------------------------------------------------------------------------------
#  glob_imgs
# ------------------------------------------------------------------------------
def glob_imgs(img_dir, num_imgs=-1, recursive=False):
    # get list of img files
    if not recursive:
        img_files = sorted(glob(os.path.join(img_dir, "*.*")))
    else:
        img_files = sorted(glob(
            os.path.join(img_dir, "**/*.*"), recursive=True))
    img_files = [img_file for img_file in img_files
                 if img_file.split('.')[-1].lower() in SUPPORT_IMG_FORMATS]
    # limit number of images
    if (num_imgs is not None) and (num_imgs != -1):
        img_files = img_files[:num_imgs]
    return img_files


# ------------------------------------------------------------------------------
#  glob_folders
# ------------------------------------------------------------------------------
def glob_folders(root_dir, recursive=False):
    if not recursive:
        folders = sorted(glob(os.path.join(root_dir, "**")))
    else:
        folders = sorted(glob(
            os.path.join(root_dir, "**/**"), recursive=True))
    return folders


# ------------------------------------------------------------------------------
#  glob_files
# ------------------------------------------------------------------------------
def glob_files(root_dir, fmt, recursive=False):
    if not recursive:
        folders = sorted(glob(os.path.join(root_dir, f"*.{fmt}")))
    else:
        folders = sorted(glob(
            os.path.join(root_dir, f"**/*.{fmt}"), recursive=True))
    return folders
