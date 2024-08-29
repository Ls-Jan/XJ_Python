__author__='Ls_Jan'
__version__='1.1.0'
__all__=['BaseCacheProxy']

from threading import Lock
from .BaseCallback import BaseCallback
from time import time,sleep

class BaseCacheProxy:
	'''
		简易的异步缓存代理，会将重复的请求合并为一个，外部调用时需要额外调用Get_TranslatedUrl转换url。
		此为抽象类，派生类仅需重写的函数有：
			- _Request(self,url:str,timeout:float)；
			- _TransUrl(self,oriUrl:str)；
		派生类异步获取到数据后需要调用_Update(reqUrl:str,data:bytes)进行保存
	'''
	class __Record:
		'''
			结构体，存储基本数据
		'''
		def __init__(self,index:int):
			self.cbs=[]#回调对象
			self.index=index#第i个url链接，虽然这数据并没价值
			self.data=b''#数据
	def __init__(self):
		self.__cache={}#请求的url<str>:record<__Record>
		self.__lock=Lock()
		self.__requestingUrls=set()#请求中的url
	def Get_UrlData(self,url:str)->bytes:
		'''
			获取指定url的缓存数据(bytes)
		'''
		return self.__cache.get(url).data
	def Get_UrlsLst(self,requesting:bool=False):
		'''
			获取所有的Url链接(list)。
			当requesting为真时仅返回请求中的url，
			当requesting为假时仅返回请求完毕后的url。
		'''
		if(requesting):
			return list(self.__requestingUrls)
		else:
			return list(self.__cache.keys())
	def Set_UrlData(self,reqUrl:str,data:bytes):
		'''
			如果已经有二进制数据那么可以直接设置而不必调用Opt_RequestUrl发出请求。
			已经发出的请求并不会被终止(也就是Opt_RequestUrl得到异步数据后会将原先设置的数据覆盖掉)，尽量不要做这种怪事。
		'''
		record=self.__cache.setdefault(reqUrl,self.__Record(len(self.__cache)))
		record.data=data
	def Opt_RequestUrl(self,reqUrl:str,cb:BaseCallback,timeout:float=0):
		'''
			异步请求url，外部最好先去调用Get_RealUrl对url进行简单的处理以避免一些问题；
			cb为回调对象；
			timeout设置超时时间(秒)；
		'''
		record=self.__cache.setdefault(reqUrl,self.__Record(len(self.__cache)))
		if(record.data):#已有数据并且数据不为空
			cb(reqUrl,record.data)
		else:#无数据，进行请求
			flag=reqUrl not in self.__requestingUrls
			self.__lock.acquire()
			record.cbs.append(cb)
			self.__requestingUrls.add(reqUrl)
			self.__lock.release()
			if(flag):
				self._Request(reqUrl,timeout)
		return reqUrl
	def Get_TranslatedUrl(self,oriUrl:str):
		'''
			使用的url并不一定就是有效的url，需要进行一步简单的转换。
		'''
		reqUrl=self._TranslateUrl(oriUrl)
		return reqUrl
	def Opt_Join(self,timeout:float=0):
		'''
			阻塞，直到所有任务都完成为止。
			内部采用sleep的方式进行阻塞。
		'''
		if(timeout>0):
			ts=time()
			while(bool(self.__requestingUrls) and time()-ts<timeout):
				sleep(0.01)
		else:
			while(bool(self.__requestingUrls)):
				sleep(0.01)
		return bool(self.__requestingUrls)
	def _Update(self,reqUrl:str,data:bytes):
		'''
			此函数供内部(包括派生类)调用。
			将得到的url数据保存并调用回调对象
		'''
		if(reqUrl not in self.__cache):#不应该出现这情况
			raise Exception('Error-UrlNotFound: ',reqUrl)
		record=self.__cache[reqUrl]
		self.__lock.acquire()
		record.data=data
		cbs=record.cbs
		record.cbs=[]
		if(reqUrl in self.__requestingUrls):
			self.__requestingUrls.remove(reqUrl)
		self.__lock.release()
		for cb in cbs:
			cb(reqUrl,data)
	def _Request(self,reqUrl:str,timeout:float=0):
		'''
			此函数供内部调用。
			请求url数据并设置超时时间。
		'''
		pass
	def _TranslateUrl(self,oriUrl:str):
		'''
			通常来说不必重写该函数，
			但总有一些异端会对url进行改动导致出现各种问题(没错说的就是QUrl.url())，
			此时就要对oriUrl进行转换，得到真正使用的reqUrl数据
		'''
		return oriUrl

