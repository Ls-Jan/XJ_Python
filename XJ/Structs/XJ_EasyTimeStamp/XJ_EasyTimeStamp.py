__author__='Ls_Jan'
__version__='1.0.0'
__all__=['XJ_EasyTimeStamp']

from time import time
class XJ_EasyTimeStamp:
	'''
		简易时间戳工具。
		时间戳以秒为单位，对应的是本地时间
	'''
	def __init__(self):
		self.__record={}
		self.Opt_AddTimeStamp()
	def Opt_AddTimeStamp(self,key:str=''):
		'''
			新增时间戳(秒)
		'''
		self.__record[key]=time()
	def Get_TimeStamp(self,key:str=''):
		'''
			获取时间戳(秒)。
			key不存在则返回None
		'''
		return self.__record[key] if key in self.__record else None
	def Get_DurationTime(self,keyStart:str='',keyEnd:str=None):
		'''
			获取两个时间戳之间的时差/经过时间(秒)。
			如果keyEnd传入None则获取当前时间。
			key不存在则返回None
		'''
		ts=self.Get_TimeStamp(keyStart)
		te=self.Get_TimeStamp(keyEnd) if keyEnd!=None else time()
		if(ts==None or te==None):
			return None
		return te-ts
	def Get_RestTime(self,timeout:float,key:str=''):
		'''
			计算目前为止指定时间戳的剩余时间(秒)，传入的timeout单位为秒。
			特别的，timeout传入0则返回0。
			key不存在则返回None。

		'''
		if(timeout==0):
			return 0
		td=self.Get_DurationTime(key)
		if(td==None):
			return None
		return timeout-td
