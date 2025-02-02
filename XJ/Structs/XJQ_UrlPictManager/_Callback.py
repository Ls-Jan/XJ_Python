
from PyQt5.QtGui import QPixmap
from .BaseFrameChange import BaseFrameChange
from ..XJ_CacheProxy.BaseCallback import BaseCallback

__all__=['_Callback']

class _Callback(BaseCallback):
	def __init__(self,fc:BaseFrameChange,failPix:QPixmap):
		self.__fc=fc
		self.__failPix=failPix
	def __call__(self,data:bytes,valid:bool):
		pix=QPixmap()
		if(valid):
			flag=pix.loadFromData(data)
			print(flag,pix.size())
			if(pix.size().isEmpty()):
				self.__fc(self.__failPix,BaseFrameChange.Type.Invalid)
			else:
				self.__fc(pix,BaseFrameChange.Type.Success)
		else:
			self.__fc(self.__failPix,BaseFrameChange.Type.Fail)

