__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_Hook']

from time import time,sleep
from PyHook3 import HookManager,KeyboardEvent,MouseEvent,HookConstants
from threading import Thread
import win32gui as WG
import win32api as WA
import win32con as WC

#PyHook3实现监控键盘鼠标操作： https://blog.csdn.net/qq_37193537/article/details/91044235
class XJ_Hook:
	'''
		全局钩子，捕获键鼠信息。
		会跑一个线程来运行钩子。
		调用Set_StatAction、Set_KeyAction、Set_Trans进行按键配置。
		调用Opt_Start启动钩子，Opt_Stop取下钩子。
	'''
	def __init__(self):
		self.__tid=None#线程id
		self.__trans={}
		self.__actionKeyboard={}
		self.__actionMouse={}
		self.__actionFixed={}
		self.__statKeyboard=0
		self.__statMouse=0
		self.__flagKeyboard=True
		self.__flagMouse=True
	def Get_IsRunning(self):
		'''
			判断钩子是否仍在运行
		'''
		return self.__tid!=None
	def Get_Stat(self,mouse:bool):
		'''
			获取当前状态
		'''
		return self.__actionMouse if mouse else self.__actionKeyboard
	def Set_Stat(self,stat:int,mouse:bool):
		'''
			设置当前状态。
			初始状态总为0。
		'''
		if(mouse):
			self.__statMouse=stat
		else:
			self.__statKeyboard=stat
	def Set_StatAction(self,stat:int,func,mouse:bool):
		'''
			设置状态动作，在进入指定状态时调用相应的函数。
			- stat：目标状态，当进入到该状态时会调用func函数；
			- func：接收一个参数，即func(stat)；
			- mouse：如果是鼠标动作则指定为真，键盘则指定为假；
		'''
		action=self.__actionMouse if mouse else self.__actionKeyboard
		action[stat]=func
	def Set_KeyAction(self,key:int,func,press:bool=None):
		'''
			设置按键动作，触发特定按键时会调用相应的函数，优先级比Set_Trans高。
			- key：当触发到特定按键时会调用func函数，鼠标的话形如HookConstants.WM_LBUTTONUP的枚举值，键盘则是形如ord('A')的大写ASCII字符对应编码；
			- press：键盘需指定press为True(按下)或是False(抬起)，鼠标则需指定为None；
			- func：接收两个参数，并返回一个int作为状态切换(返回None则不变化)，即func(stat,key)->int
		'''
		self.__actionFixed[self.__Get_TransTuple(None,key,press)]=func
	def Set_Trans(self,start:int,key:int,next:int,press:bool=None):
		'''
			设置转换。
			- start：当前状态；
			- next：在当前状态下满足转换条件(key和press)后的下一状态；
			- press：键盘需指定press为True(按下)或是False(抬起)，鼠标则需指定为None；
			- key：鼠标的话形如HookConstants.WM_LBUTTONUP的枚举值，键盘则是虚拟键形如ord('A')；
		'''
		self.__trans[self.__Get_TransTuple(start,key,press)]=next
	def Opt_Start(self,mouse:bool=True,keyboard:bool=True):
		'''
			启动钩子。
			可选择性的启动键鼠钩子
		'''
		if(not self.__tid):
			self.__flagKeyboard=keyboard
			self.__flagMouse=mouse
			if(mouse or keyboard):
				Thread(target=self.__ThreadFunc).start()
			sleep(0.01)#防突刺
	def Opt_Stop(self):
		'''
			结束钩子
		'''
		if(self.__tid):
			WG.PostThreadMessage(self.__tid,WC.WM_QUIT,0,0)
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
		hm = HookManager()
		if(self.__flagMouse):
			hm.MouseAll=self.__MouseHook
			hm.HookMouse()#启动挂钩
		if(self.__flagKeyboard):
			hm.KeyAll=self.__KeyboardHook
			hm.HookKeyboard()#启动挂钩
		WG.PumpMessages()#进入消息循环，直到调用WG.PostThreadMessage(tid,WC.WM_QUIT,0,0)
		if(self.__flagMouse):
			hm.UnhookMouse()#关闭挂钩
		if(self.__flagKeyboard):
			hm.HookKeyboard()
		self.__tid=None
	def __KeyboardHook(self,event:KeyboardEvent):
		'''
			键盘的钩子函数
		'''
		key=event.KeyID
		stat=self.__statKeyboard
		action=self.__actionKeyboard
		pressed=not bool(event.IsTransition())
		statNext=self.__trans.get(self.__Get_TransTuple(stat,key,pressed),None)
		func=self.__actionFixed.get(self.__Get_TransTuple(None,key,pressed),None)
		if(func!=None):
			statNext=func(stat,key)
		if(statNext!=None and stat!=statNext):
			stat=statNext
			func=action.get(stat,lambda stat:None)
			func(stat)
			self.__statKeyboard=stat
		return True
	def __MouseHook(self,event:MouseEvent):
		'''
			鼠标的钩子函数
		'''
		key=event.Message
		stat=self.__statMouse
		action=self.__actionMouse
		pressed=None
		statNext=self.__trans.get(self.__Get_TransTuple(stat,key,pressed),None)
		func=self.__actionFixed.get(self.__Get_TransTuple(None,key,pressed),None)
		if(func!=None):
			statNext=func(stat,key)
		if(statNext!=None and stat!=statNext):
			stat=statNext
			func=action.get(stat,lambda stat:None)
			func(stat)
			self.__statMouse=stat
		return True
	def __Get_TransTuple(self,start:int,key:int,press:bool):
		'''
			为了避免出现无意间引入低级错误而设置的垃圾函数
		'''
		return (start,key,press)



