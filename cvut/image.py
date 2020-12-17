import mmcv
import numpy as np


#------------------------------------------------------------------------------
#  impt2np
#------------------------------------------------------------------------------
def impt2np(image):
	image = image[0].cpu().numpy().transpose((1,2,0))
	return image


#------------------------------------------------------------------------------
#  imdenormalize
#------------------------------------------------------------------------------
def imdenormalize(image, mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], scale_255=False):
	if scale_255:
		image = np.clip(((image * std + mean) * 255.), 0, 255).astype('uint8')
	else:
		image = np.clip(image * std + mean, 0, 255).astype('uint8')
	return image


#------------------------------------------------------------------------------
#  imwrite
#------------------------------------------------------------------------------
def imwrite(image, outfile):
	mmcv.imwrite(image, outfile)
	print("[cvut] Image is saved at {}".format(outfile))
