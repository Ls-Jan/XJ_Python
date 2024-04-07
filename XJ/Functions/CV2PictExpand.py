

__version__='1.0.0'
__author__='Ls_Jan'

import numpy as np

__all__=['CV2PictExpand']

def CV2PictExpand(im:np.ndarray,pix:tuple=None):
	'''
		将一个图片扩展为正方形，pix指定扩展后空白部分的像素颜色(默认黑色透明)
	'''
	if(im.shape[0]!=im.shape[1]):
		s=max(im.shape[:2])
		imNew=np.zeros((s,s,im.shape[2]),dtype=im.dtype)
		if(pix!=None and len(pix)==imNew.shape[2]):
			imNew[:,:,:]=pix
		offset=[int((s-val)/2) for val in im.shape[:2]]
		imNew[offset[0]:offset[0]+im.shape[0],offset[1]:offset[1]+im.shape[1],:]=im
		im=imNew
	return im

