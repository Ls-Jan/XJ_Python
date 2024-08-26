

__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_QUrlCacheProxy']

import os
from PyQt5.QtCore import QUrl,QByteArray
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
		req.setUrl(self.__Get_QUrl(url))
		req.setTransferTimeout(timeout)
		self.__manager.get(req)
	def __Func_Request(self,reply:QNetworkReply):
		'''
			该函数供线程调用
		'''
		url=reply.url().url()
		data=reply.readAll().data()
		self._Update(url,data)
	def __Get_QUrl(self,url:str):
		#以弯弯绕的方式将本地文件路径改为用“file”前缀的url
		path=QByteArray.fromPercentEncoding(QByteArray((url.encode()))).data().decode()#因为QUrl会将百分号进行转义，这一步不能跳
		if(os.path.exists(path)):
			url=QByteArray(path.encode()).toPercentEncoding().data().decode()#将路径改为百分号编码
			url=QUrl(f'file:///{url}')
		return url
	def _TransUrl(self,url:str):
		return self.__Get_QUrl(url).url()

