

__version__='1.0.1'
__author__='Ls_Jan'
__all__=['XJ_QUrlCacheProxy']

import os
from PyQt5.QtCore import QUrl,QByteArray
from PyQt5.QtNetwork import QNetworkRequest,QNetworkAccessManager,QNetworkReply
from .BaseCacheProxy import BaseCacheProxy
from typing import Dict

class XJ_QUrlCacheProxy(BaseCacheProxy):
	'''
		使用PyQt5相关模块进行数据请求。
		QNetworkAccessManager：https://blog.csdn.net/CodeWorld1999/article/details/139326812
	'''
	def __init__(self):
		super().__init__()
		manager=QNetworkAccessManager()
		manager.finished.connect(self.__Func_Request)
		self.__manager:QNetworkAccessManager=manager
		self.__record:Dict[QNetworkReply,tuple]={}#tuple记录(url,payload)
	def _Request(self,reqUrl:str,timeout:float=0,payload:str=None):
		req=QNetworkRequest()
		req.setHeader(QNetworkRequest.UserAgentHeader,"RT-Thread ART")
		req.setUrl(QUrl(self.__TranslateUrl(reqUrl)))
		req.setTransferTimeout(timeout)
		if(payload):
			rep=self.__manager.post(req,payload)
		else:
			rep=self.__manager.get(req)
		self.__record[rep]=(reqUrl,payload)
	def __Func_Request(self,reply:QNetworkReply):
		'''
			该函数供线程调用
		'''
		url,payload=self.__record.pop(reply)#这才是原本的url。reply.url().url()返回的url不一定与原始请求一致
		data=reply.readAll().data()
		self._Update(url,data,payload)
	@staticmethod
	def __TranslateUrl(url:str):
		'''
			将本地文件路径改为用“file”前缀的url
		'''
		if(os.path.exists(url)):
			path=os.path.realpath(url)
			url=QByteArray(path.encode()).toPercentEncoding().data().decode()#将路径改为百分号编码
			url=QUrl(f'file:///{url}').url()
		return url

