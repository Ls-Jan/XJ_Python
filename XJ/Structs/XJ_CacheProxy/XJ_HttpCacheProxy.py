__author__='Ls_Jan'
__version__='1.0.1'
__all__=['XJ_HttpCacheProxy']

import requests
from concurrent.futures import ThreadPoolExecutor
from .BaseCacheProxy import BaseCacheProxy

class XJ_HttpCacheProxy(BaseCacheProxy):
	'''
		使用requests以及concurrent模块进行网络数据异步请求
	'''
	def __init__(self,requestCount:int=None):
		super().__init__()
		self.__session=requests.session()
		self.__pool=ThreadPoolExecutor(requestCount)#使用线程池：https://blog.csdn.net/xpt211314/article/details/109543014
	def _Request(self,reqUrl:str,timeout:float=0,payload:str=None):
		self.__pool.submit(self.__Func_Request,reqUrl,timeout,payload)
	def __Func_Request(self,url:str,timeout:float=0,payload:str=None):
		'''
			该函数供线程调用
		'''
		if(payload):
			resp=self.__session.post(url,payload,timeout=timeout if timeout>0 else None)
		else:
			resp=self.__session.get(url,timeout=timeout if timeout>0 else None)
		self._Update(url,resp.content,payload)
		
