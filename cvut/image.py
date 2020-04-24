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
def imdenormalize(image, mean, std, scale_255=True):
	if scale_255:
		image = np.clip(((image * std + mean) * 255.), 0, 255).astype('uint8')
	else:
		image = np.clip(image * std + mean, 0, 255).astype('uint8')
	return image
