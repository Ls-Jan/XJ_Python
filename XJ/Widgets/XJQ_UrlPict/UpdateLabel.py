__version='1.0.0'
__author__='Ls_Jan'
__all__=['UpdateLabel']

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from ...Structs.XJ_CacheProxy.BaseCallback import BaseCallback
from .ValueShrink import ValueShrink



class UpdateLabel(BaseCallback):
	def __init__(self,lb:QLabel,pictFail:QPixmap,flag:list=None,func_shrinkedSize=None):
		'''
			传入一个列表flag以判断pixmap的有效性，flag为空则说明数据无效；
			如果func_shrinkedSize为空则不调整图片大小，这里附赠一个默认的大小调节函数UpdateLabel.Get_ShrinkedSize
		'''
		if(flag==None):
			flag=[]
		flag.clear()
		self.__lb=lb
		self.__pictFail=pictFail
		self.__flag=flag
		self.__shrink=func_shrinkedSize
	def __call__(self, data: bytes):
		self.__flag.clear()
		if(data):
			pix=QPixmap()
			pix.loadFromData(data)
			if(self.__shrink):
				size=self.__shrink((pix.width(),pix.height()))
				pix=pix.scaled(*size)
			self.__flag.append(None)
		else:
			pix=self.__pictFail
		self.__lb.setPixmap(pix)
	@staticmethod
	def Get_ShrinkedSize(size):
		'''
			预置函数，获取缩小后的大小
		'''
		return ValueShrink.GroupShrink(size,ValueShrink(150,50,5),ValueShrink(100,50,6))
