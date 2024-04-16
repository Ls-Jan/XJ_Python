
from typing import Union
from PyQt5.QtGui import QImage,QPixmap
import numpy as np

__all__=['CV2FromQPixmap']
def CV2FromQPixmap(pix:Union[QPixmap,QImage]):#pix是RGBA四通道QPixmap。不使用PIL.Image模块
	'''
		arr对应3通/4通图片。这里不使用PIL方法。

		https://blog.csdn.net/weixin_44431795/article/details/122016214
		https://deepinout.com/numpy/numpy-questions/700_numpy_qimage_to_numpy_array_using_pyside.html#ftoc-heading-3
	'''
	h,w=pix.height(),pix.width()
	im=QImage(pix) if isinstance(pix,QPixmap) else pix
	buffer = im.constBits()
	depth=int(im.depth()/8)
	buffer.setsize(h*w*depth)
	arr = np.frombuffer(buffer, dtype=np.uint8).reshape((h,w,depth))
	return arr.copy()


