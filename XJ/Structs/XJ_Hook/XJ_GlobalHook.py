__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_GlobalHook']

from time import time,sleep
from PyHook3 import HookManager
from threading import Thread
import win32gui as WG
import win32api as WA
import win32con as WC

#PyHook3实现监控键盘鼠标操作： https://blog.csdn.net/qq_37193537/article/details/91044235
class XJ_GlobalHook:
	'''
		全局钩子，捕获键鼠信息。
		会跑一个线程来运行钩子。
		调用Opt_Start启动钩子，Opt_Stop取下钩子。
	'''
	def __init__(self,funcMouse=None,funcKeyboard=None):
		'''
			- funcMouse(PyHook3.MouseEvent)；
			- funcKeyboard(PyHook3.KeyboardEvent)；
			根据实际情况传入钩子函数。
		'''
		self.__tid=None#线程id
		self.__funcMouse=funcMouse
		self.__funcKeyboard=funcKeyboard
	def Opt_Start(self):
		'''
			启动钩子
		'''
		if(not self.__tid):
			Thread(target=self.__ThreadFunc).start()
			sleep(0.01)#防突刺
	def Opt_Stop(self):
		'''
			结束钩子
		'''
		if(self.__tid):
			WG.PostThreadMessage(self.__tid,WC.WM_QUIT,0,0)
	def Get_IsRunning(self):
		'''
			判断钩子是否仍在运行
		'''
		return self.__tid!=None
	def Opt_Join(self,mTime:int=0):
		'''
			阻塞等待，mTime为毫秒。
			只要钩子仍在运行就会一直阻塞。
		'''
		cTime=time()+mTime/1000
		keepRunning=lambda:cTime>time() if mTime>0 else lambda:True
		while(self.__tid and keepRunning()):#懒得找，直接用这种方式堵
			sleep(0.01)
	def __ThreadFunc(self):#线程函数
		self.__tid=WA.GetCurrentThreadId()
		if(self.__funcKeyboard or self.__funcMouse):
			hm = HookManager()
			if(self.__funcMouse):
				hm.MouseAll=self.__funcMouse
				hm.HookMouse()#启动挂钩
			if(self.__funcKeyboard):
				hm.KeyAll=self.__funcKeyboard
				hm.HookKeyboard()
			WG.PumpMessages()#进入消息循环，直到调用WG.PostThreadMessage(tid,WC.WM_QUIT,0,0)
			if(self.__funcMouse):
				hm.UnhookMouse()#关闭挂钩
			if(self.__funcKeyboard):
				hm.HookKeyboard()
		self.__tid=None

