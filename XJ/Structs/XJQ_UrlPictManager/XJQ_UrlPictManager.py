__author__='Ls_Jan'
__version__='1.1.0'
__all__=['XJQ_UrlPictManager']


from PyQt5.QtCore import QObject,QSize
from PyQt5.QtGui import QPixmap,QMovie
from .BaseFrameChange import BaseFrameChange
from ._Callback import _Callback
from ..XJ_CacheProxy.XJ_QUrlCacheProxy import XJ_QUrlCacheProxy,BaseCacheProxy
from typing import Dict,Set

class XJQ_UrlPictManager(QObject):
	'''
		外链图片管理器，使图片在请求过程中有加载效果。
	'''
	__timeout:int=0
	__failPict:QPixmap=None
	__loadingMovie:QMovie=None
	__cacheProxy:BaseCacheProxy=None
	__record:Dict[tuple,Set[BaseFrameChange]]=None#记录相应的FrameChange以便发送加载动图帧
	def __init__(self,loadingMovie:QMovie,failPict:QPixmap,cacheProxy:BaseCacheProxy=None,timeout:int=0):
		'''
			loadingMovie：加载动图；
			failPict：加载失败图；
			cacheProxy：缓存代理，默认使用XJ_QUrlCacheProxy；
			timeout：超时时长(秒)，<=0的视为无限时长；
		'''
		super().__init__()
		self.__loadingMovie=loadingMovie
		self.__failPict=failPict
		self.__cacheProxy=cacheProxy if cacheProxy else XJ_QUrlCacheProxy()
		self.__timeout=timeout
		self.__record={}
		loadingMovie.stop()
		loadingMovie.jumpToFrame(0)
		loadingMovie.frameChanged.connect(self.__Opt_UpdateFrame)
	def __Opt_UpdateFrame(self):
		'''
			发送famreChanged信号，如果当前无正在请求的数据则会暂停QMovie
		'''
		requesting=self.__cacheProxy.Get_UrlHistory().requesting.copy()
		if(requesting):
			loadPix=self.__loadingMovie.currentPixmap()
			for uInfo in requesting:
				for fc in self.__record[uInfo]:
					fc(loadPix,fc.Type.Loading)
		else:
			self.__loadingMovie.stop()
	def Opt_RequestUrl(self,url:str,fc:BaseFrameChange,payload:str=None,data:bytes=None):
		'''
			请求图片数据。
			如果已有图片数据则可指定data进行设置。
		'''
		self.__record.setdefault((url,payload),set()).add(fc)
		self.__loadingMovie.start()
		if(data):
			self.__cacheProxy.Set_UrlData(url,data,payload)
		self.__cacheProxy.Opt_RequestUrl(url,_Callback(fc,self.__failPict),self.__timeout,payload)
	def Get_CacheProxy(self):
		'''
			返回缓存代理(BaseFrameChange)
		'''
		return self.__cacheProxy
	def Get_RequestingUrl(self)->set:
		'''
			返回正在请求中的url
		'''
		return self.__cacheProxy.Get_UrlHistory().requesting.copy()
	def Get_UrlPict(self,url:str,payload:str=None):
		'''
			获取url的当前图片(QPixmap)以及加载状态(BaseFrameChange.Type)。
			未曾请求过的数据会返回None
		'''
		uInfo=(url,payload)
		if(uInfo in self.__record):
			fc=next(iter(self.__record[uInfo]))
			return fc.Get_Pixmap(),fc.Get_Type()
		return None

