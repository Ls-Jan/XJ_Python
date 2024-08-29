__version__='1.0.0'
__author__='Ls_Jan'
__all__=['UrlPictConfig']

from PyQt5.QtGui import QMovie,QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication
from ...Structs.XJ_CacheProxy.XJ_QUrlCacheProxy import XJ_QUrlCacheProxy
from ...Structs.XJ_CacheProxy import BaseCacheProxy

class UrlPictConfig:
	'''
		保存着两份数据(加载动画/加载失败)，以及一份缓存代理，供XJQ_UrlPict使用
	'''
	def __init__(self,size:tuple,dataWait:QMovie=None,dataFail:QPixmap=None,cacheProxy:BaseCacheProxy=None):
		'''
			size为2-tuple，作为宽高；
			cp为缓存代理，传入None则创建XJ_QUrlCacheProxy对象；
			dataWait是加载动画，是QMovie对象；
			dataFail是失败图片，是QPixmap对象；
		'''
		self.__cacheProxy=cacheProxy if cacheProxy else XJ_QUrlCacheProxy() 
		self.__size=size
		self.__pictWait=None
		self.__pictFail=None
		self.pictWait=dataWait
		self.pictFail=dataFail
	@property
	def cacheProxy(self):
		return self.__cacheProxy
	@property
	def size(self):
		return self.__size
	@property
	def pictWait(self):
		return self.__pictWait
	@property
	def pictFail(self):
		return self.__pictFail
	@pictWait.setter
	def pictWait(self,data:QMovie):
		'''
			设置加载动画。
		'''
		mv=data if data else QMovie()
		if(self.size):
			mv.setScaledSize(QSize(*self.size))
		mv.start()
		self.__pictWait=mv
	@pictFail.setter
	def pictFail(self,data:QPixmap):
		'''
			设置失败图片。
		'''
		pix=data if data else QApplication.style().standardIcon(25).pixmap(16,16)

		if(pix and self.size):
			pix=pix.scaled(QSize(*self.size))
		self.__pictFail=pix


