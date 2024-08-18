

__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_QUrlCacheProxy']

from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkRequest,QNetworkAccessManager,QNetworkReply
from .BaseCacheProxy import BaseCacheProxy

class XJ_QUrlCacheProxy(BaseCacheProxy):
	def __init__(self):
		super().__init__()
		manager=QNetworkAccessManager()
		manager.finished.connect(self.__Func_Request)
		self.__manager=manager
	def _Request(self, url: str, timeout: int=0):
		req=QNetworkRequest()
		req.setHeader(QNetworkRequest.UserAgentHeader,"RT-Thread ART")
		req.setUrl(QUrl(url))
		req.setTransferTimeout(timeout)
		self.__manager.get(req)
	def __Func_Request(self,reply:QNetworkReply):
		'''
			该函数供线程调用
		'''
		url=reply.url().url()
		data=reply.readAll().data()
		self._Update(url,data)
		
