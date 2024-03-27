
import numpy as np
import cv2

def Get_GradientPict(color,*,left=False,top=False,right=False,bottom=False):
	'''
		专门生成256*256*4的纯色alpha渐变图片，作为图片处理的测试样例。
	'''
	color=[*color[:3],0]
	extend=[int(top),int(bottom),int(left),int(right)]
	flag=False
	for i in range(4):
		if(extend[i]):
			if(flag):
				extend[i]=0
			else:
				flag=True
	if(sum(extend)==0):
		extend[3]=1
	pict=np.ones((256,1,4) if extend[2] or extend[3] else (1,256,4),dtype=np.uint8)
	for i in range(1,256):
		color[-1]=i
		pict=cv2.copyMakeBorder(pict,*extend,cv2.BORDER_CONSTANT,value=color)
	return pict




