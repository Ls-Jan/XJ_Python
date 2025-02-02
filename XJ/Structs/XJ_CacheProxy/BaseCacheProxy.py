__author__='Ls_Jan'
__version__='1.3.0'
__all__=['BaseCacheProxy']

from .BaseCallback import BaseCallback
from ._Record import _Record
from ._Urls import _Urls
from threading import Lock
from time import time,sleep
from typing import Dict

class BaseCacheProxy:
	'''
		简易的异步缓存代理，会将重复的请求合并为一个。
		此为抽象类，派生类仅需重写的函数有：
			- _Request(self,url:str,timeout:float=0,payload:str=None)；
		_Request这个函数用于数据请求，除此之外派生类需在合适的地方插入_Update的调用，_Update用于数据获取后的数据同步
	'''

	def __init__(self,dataValidTest=lambda data:bool(data)):
		'''
			dataValidTest用于判断url请求返回的数据是否有效
		'''
		self.__cache:Dict[tuple,_Record]={}#(请求的url<str>,携带数据的hash值):record<_Record>
		self.__dataValidTest=dataValidTest
		self.__dataLock=Lock()#数据修改时强制原子性
		self.__busyLock=Lock()#将存在修改行为的操作强制同步，因为不知道函数会在什么环境下被调用(防一手异步调用)
		self.__urls=_Urls()#记录三种url：请求中、请求成功、请求失败
	def Opt_Clear(self):
		'''
			清空缓存记录。
			无法清除正在进行的请求。
		'''
		self.__busyLock.acquire()
		enable=[]
		self.__dataLock.acquire()
		for key,record in self.__cache.items():
			if(not record.cbs):
				enable.append(key)
		for key in enable:#只移除回调为空的，非空说明数据仍在请求。
			self.__cache.pop(key)
		self.__urls.success.clear()
		self.__urls.fail.clear()
		self.__dataLock.release()
		self.__busyLock.release()
	def Get_UrlData(self,reqUrl:str,payload:str=None)->bytes:
		'''
			获取指定url的缓存数据(bytes)
		'''
		uInfo=(reqUrl,payload)
		self.__dataLock.acquire()
		data=self.__cache.get(uInfo).data if uInfo in self.__cache else b''
		self.__dataLock.release()
		return data
	def Get_UrlHistory(self):
		'''
			获取所有的url请求(url+payload)。
			返回的对象包含三个属性，分别是：请求中(requesting)、请求成功(success)、请求失败(fail)。
			返回对象的数据不可修改。
		'''
		return self.__urls
	def Set_UrlData(self,reqUrl:str,data:bytes,payload:str=None):
		'''
			如果已经有二进制数据那么可以直接设置而不必调用Opt_RequestUrl发出请求。
			设置成功则返回True。
			发出的请求不会被终止，同时使用该函数也不会成功设置数据，因此Set_UrlData尽量在Opt_RequestUrl前调用。
		'''
		uInfo=(reqUrl,payload)
		self.__dataLock.acquire()
		record=self.__cache.setdefault(uInfo,_Record())
		flag=bool(record.cbs)#也可以是reqUrl in self.__urls.requesting
		if(not flag):
			record.data=data
			record.valid=self.__dataValidTest(data)
		if(record.valid):
			self.__urls.fail.discard(uInfo)
			self.__urls.success.add(uInfo)
		else:
			self.__urls.success.discard(uInfo)
			self.__urls.fail.add(uInfo)
		self.__dataLock.release()
		return flag
	def Opt_RequestUrl(self,reqUrl:str,cb:BaseCallback,timeout:float=0,payload:str=None):
		'''
			异步请求url，cb为回调对象；
			timeout设置超时时间(秒)；
			payload为附带的请求信息(默认不带，使用get方式)；
		'''
		uInfo=(reqUrl,payload)
		self.__busyLock.acquire()
		self.__dataLock.acquire()
		record=self.__cache.setdefault(uInfo,_Record())
		self.__dataLock.release()
		if(record.valid):#数据有效，直接调用
			cb(record.data,True)
		else:#数据无效，进行请求
			self.__dataLock.acquire()
			exist=bool(record.cbs)#判断当前是否存在请求
			record.cbs.append(cb)
			self.__dataLock.release()
			if(not exist):
				self._Request(reqUrl,timeout)
				self.__urls.fail.discard(uInfo)
				self.__urls.requesting.add(uInfo)
		self.__busyLock.release()
		return reqUrl
	def Opt_Join(self,timeout:float=0,reqUrl:str=None,payload:str=None):
		'''
			阻塞，直到所有任务都完成为止，如果timeout<=0则视为无限时长。
			内部采用sleep的方式进行阻塞。
			可以指定reqUrl以阻塞特定请求完成。
		'''
		self.__busyLock.acquire()#确保阻塞过程中不会出现诸如Opt_RequestUrl的数据修改行为
		if(timeout<0):
			timeout=2**30
		ts=time()
		uInfo=(reqUrl,payload)
		while(time()-ts<timeout and (uInfo in self.__urls.requesting if reqUrl else self.__urls.requesting)):
			sleep(0.01)
		self.__busyLock.release()
		return bool(self.__urls.requesting)
	def _Update(self,reqUrl:str,data:bytes,payload:str=None):
		'''
			此函数供内部(包括派生类)调用。
			将得到的url数据保存并调用回调对象
		'''
		uInfo=(reqUrl,payload)
		if(uInfo not in self.__cache):#不应该出现这情况
			raise Exception('Error-UrlNotFound: ',uInfo)
		record=self.__cache[uInfo]
		valid=self.__dataValidTest(data)
		self.__dataLock.acquire()
		record.data=data
		record.valid=valid
		cbs=record.cbs
		record.cbs=[]
		self.__dataLock.release()
		for cb in cbs:
			cb(data,valid)
		self.__urls.requesting.discard(uInfo)
		if(valid):
			self.__urls.success.add(uInfo)
		else:
			self.__urls.fail.add(uInfo)
	def _Request(self,reqUrl:str,timeout:float=0,payload:str=None):
		'''
			此函数供内部调用，派生类需完成相应的异步url请求。
			异步请求url；
			timeout设置超时时间(秒)；
			payload为附带的请求信息(默认不带，使用get方式)；
		'''
		pass

