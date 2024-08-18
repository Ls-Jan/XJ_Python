__author__='Ls_Jan'
__version__='1.0.0'
__all__=['BaseCacheProxy']

from threading import Lock
from .BaseCallback import BaseCallback
from time import time,sleep

class BaseCacheProxy:
	'''
		简易的异步缓存代理，会将重复的请求合并为一个。
		此为抽象类，派生类仅需重写的函数有：
			- _Request(self,url:str,timeout:float)；
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
		self.__cache={}#url<str>:record<__Record>
		self.__lock=Lock()
		self.__urls=set()
	def Get_UrlData(self):
		'''
			获取url的缓存数据
		'''
		rst={}
		for url,record in self.__cache.items():
			rst[url]=record.data
		return rst
	def Get_RequestUrls(self):
		'''
			获取正在请求中的url，虽然没啥意义。
		'''
		return self.__urls.copy()
	def Set_UrlData(self,url:str,data:bytes):
		'''
			如果已经有二进制数据那么可以直接设置而不必调用Opt_GetUrl发出请求。
			已经发出的请求并不会被终止(也就是Opt_GetUrl得到异步数据后会将原先设置的数据覆盖掉)，尽量不要做这种怪事。
		'''
		record=self.__cache.setdefault(url,self.__Record(len(self.__cache)))
		record.data=data
	def Opt_GetUrl(self,url:str,cb:BaseCallback,timeout:float=0):
		'''
			异步请求url；
			cb为回调对象；
			timeout设置超时时间(秒)；
		'''
		record=self.__cache.setdefault(url,self.__Record(len(self.__cache)))
		if(record.data):#已有数据
			cb(record.data)
		else:#无数据，进行请求
			flag=url not in self.__urls
			self.__lock.acquire()
			record.cbs.append(cb)
			self.__urls.add(url)
			self.__lock.release()
			if(flag):
				self._Request(url,timeout)
	def Opt_Join(self,timeout:float=0):
		'''
			阻塞，直到所有任务都完成为止。
			内部采用sleep的方式进行阻塞。
		'''
		if(timeout>0):
			ts=time()
			while(bool(self.__urls) and time()-ts<timeout):
				sleep(0.01)
		else:
			while(bool(self.__urls)):
				sleep(0.01)
		return bool(self.__urls)
	def _Update(self,url:str,data:bytes):
		'''
			此函数供内部(包括派生类)调用。
			将得到的url数据保存并调用回调对象
		'''
		if(url not in self.__cache):#不应该出现这情况
			raise Exception('Error-UrlNotFound: ',url)
		record=self.__cache[url]
		self.__lock.acquire()
		record.data=data
		cbs=record.cbs
		record.cbs=[]
		if(url in self.__urls):
			self.__urls.remove(url)
		self.__lock.release()
		for cb in cbs:
			cb(data)
	def _Request(self,url:str,timeout:float=0):
		'''
			此函数供内部调用。
			请求url数据并设置超时时间
		'''
		pass



