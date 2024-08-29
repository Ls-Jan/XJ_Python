__author__='Ls_Jan'
__version__='1.0.0'
__all__=['XJQ_UrlPictManager']


from PyQt5.QtCore import QObject,pyqtSignal,QMutex,QSize
from PyQt5.QtGui import QPixmap,QMovie
from ..XJ_CacheProxy.BaseCallback import BaseCallback
from ..XJ_CacheProxy.XJ_QUrlCacheProxy import XJ_QUrlCacheProxy
from ..XJ_CacheProxy.BaseCacheProxy import BaseCacheProxy


class XJQ_UrlPictManager(QObject):
	'''
		外链图片管理器，将图片加载过程更加的分化。
		会发出三种信号：
			- pixChanged(set)：图片信息发生变化的链接；
			- requestSuccess(str)：请求成功的链接；
			- requestFail(str)：请求失败的链接；
	'''
	pixChanged=pyqtSignal(set)
	requestSuccess=pyqtSignal(str)
	requestFail=pyqtSignal(str)
	class __Callback(BaseCallback):#正是因为无法顺利的多继承，才硬生生的扯出这一坨东西，虽然不雅但问题不大
		def __init__(self,mutex:QMutex,finishUrls:set,failUrls:set,urls:map,failPict:QPixmap):
			self.__finishUrls=finishUrls
			self.__failUrls=failUrls
			self.__urls=urls
			self.__failPict=failPict
			self.__mutex=mutex
		def __call__(self,url:str,data:bytes):
			self.__mutex.lock()
			self.__finishUrls.add(url)
			if(data):
				pix=QPixmap()
				pix.loadFromData(data)
				self.__urls[url]=pix
			else:
				self.__urls[url]=self.__failPict
				self.__failUrls.add(url)
			self.__mutex.unlock()
	__timeout:int=0
	__failPict:QPixmap=None
	__cacheProxy:BaseCacheProxy=None
	__loadingMovie:QMovie=None
	def __init__(self,loadingMovie:QMovie,failPict:QPixmap,cacheProxy:BaseCacheProxy=None,timeout:int=0):
		super().__init__()
		self.__mutex=QMutex()
		self.__loadingMovie=loadingMovie
		self.__failPict=failPict
		self.__cacheProxy=cacheProxy if cacheProxy else XJ_QUrlCacheProxy()
		self.__timeout=timeout
		self.__urlsRequesting=set()#请求中
		self.__urlsFinished=set()#请求完毕
		self.__urlsFail=set()#失败
		self.__urlsPix=dict()#成功。{url<str>:pix<QPixmap>}
		mv=loadingMovie
		mv.stop()
		mv.jumpToFrame(0)
		mv.frameChanged.connect(self.__Opt_UpdateFrame)
	def __Opt_UpdateFrame(self):
		'''
			发送famreChanged信号，如果当前无正在请求的数据则会暂停QMovie
		'''
		urlsRequesting=self.__urlsRequesting.copy()
		urlsFinished=self.__urlsFinished.copy()
		if(urlsRequesting):
			self.__mutex.lock()
			for url in urlsRequesting:
				if(url not in urlsFinished):
					self.__urlsPix[url]=self.__loadingMovie.currentPixmap()
			self.__urlsRequesting.difference_update(urlsFinished)
			self.__urlsFinished.clear()
			self.__mutex.unlock()
			for url in urlsRequesting:
				if(url in urlsFinished):
					if(url not in self.__urlsFail):
						self.requestSuccess.emit(url)
					else:
						self.requestFail.emit(url)
			self.pixChanged.emit(self.__urlsRequesting.copy())
		else:
			self.__loadingMovie.stop()
	def Opt_RequestUrl(self,url:str,data:bytes=None):
		'''
			请求图片数据，返回实际请求的url。
			如果已有图片数据则可指定data进行设置
		'''
		url=self.__cacheProxy.Get_TranslatedUrl(url)
		self.__mutex.lock()
		self.__urlsPix[url]=self.__loadingMovie.currentPixmap()
		self.__urlsRequesting.add(url)
		self.__mutex.unlock()
		self.__loadingMovie.start()
		if(data):
			self.__cacheProxy.Set_UrlData(url,data)
		self.__cacheProxy.Opt_RequestUrl(url,self.__Callback(self.__mutex,self.__urlsFinished,self.__urlsFail,self.__urlsPix,self.__failPict),self.__timeout)
		return url
	def Get_Size(self,url:str)->QSize:
		'''
			获取图片大小(QSize)
		'''
		return self.__urlsPix[url].size()
	def Get_IsValid(self,url:str)->bool:
		'''
			判断图片是否有效
		'''
		return url not in self.__urlsRequesting and url not in self.__urlsFail
	def Get_RequestingUrl(self)->set:
		'''
			返回正在请求中的url
		'''
		return self.__urlsRequesting
	def Get_AllUrls(self):
		'''
			获取所有的url
		'''
		return set(self.__urlsPix)
	def Get_UrlPict(self,url:str)->QPixmap:
		'''
			获取url的当前图片
		'''
		pix=self.__urlsPix.get(url)
		return pix if pix else QPixmap()



