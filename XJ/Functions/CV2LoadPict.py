
import cv2
import numpy as np

__all__=['CV2LoadPict']
def CV2LoadPict(path):
	'''
		cv2读取中文路径图片：https://www.zhihu.com/question/67157462/answer/251754530
	'''
	return cv2.imdecode(np.fromfile(path,dtype=np.uint8),cv2.IMREAD_UNCHANGED)

