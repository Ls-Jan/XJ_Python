
from typing import Union
from PyQt5.QtCore import QSize

def GetShrunkSize(size:Union[tuple,QSize],maxSize:Union[tuple,QSize],returnQSize:bool=True):
	'''
		获取缩小的size以及一个bool(该布尔值仅在返回的size与传入时不一致时为真)。
		returnQSize为真时将返回QSize，否则直接返回tuple。

		(该函数主要用于图片比例缩放，函数虽然鸡肋但奈何它有点用，就单独抽离出来了
	'''
	if(isinstance(size,QSize)):
		size=(size.width(),size.height())
	if(isinstance(maxSize,QSize)):
		maxSize=(maxSize.width(),maxSize.height()) if maxSize.isValid() else size
	rate=[maxSize[i]/size[i] for i in range(2)]
	rate=min(rate)
	if(rate<1):
		size=[int(s*rate) for s in size]
	if(returnQSize):
		size=QSize(*size)
	return size,rate<1


