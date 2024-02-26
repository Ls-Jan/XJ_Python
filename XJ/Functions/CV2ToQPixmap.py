
from PyQt5.QtGui import QImage,QPixmap

__all__=['CV2ToQPixmap']

def CV2ToQPixmap(arr):
	'''
		arr对应3通/4通图片。这里不使用PIL方法。

		https://blog.csdn.net/weixin_44431795/article/details/122016214
		https://blog.csdn.net/comedate/article/details/121259033
	'''
	shape=(*arr.shape,1)[:3]#防灰度图
	format={
		1:QImage.Format_Grayscale8,
		2:QImage.Format_Grayscale16,
		3:QImage.Format_RGB888,
		4:QImage.Format_RGBA8888,
	}

	img=QImage(arr.data, shape[1], shape[0], shape[1]*shape[2], format[shape[2]])
	return QPixmap(img)


