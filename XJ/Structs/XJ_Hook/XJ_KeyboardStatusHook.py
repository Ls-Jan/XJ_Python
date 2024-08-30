__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_KeyboardStatusHook']

from .XJ_GlobalHook import XJ_GlobalHook
from PyHook3 import KeyboardEvent

class XJ_KeyboardStatusHook(XJ_GlobalHook):
	'''
		键盘钩子。
		是XJ_GlobalHook的特化，额外封装了状态转换功能。
	'''
	def __init__(self,*statusTrans:tuple):
		'''
			- statusTrnas格式为(oldStatus,key,newStatus)，
				含义为：在旧状态oldStatus下，如果XJ_GlobalHook.keyID的值与key[0]相等，并且按键状态(按下/抬起)与key[1]一致时，那么将进入到新状态newStatus。
				补充：key[0]为虚拟键值，key[1]为按键按下的布尔值，如果key[1]不存在则无论按键是否按下都会进入新状态。
					特别的，可以直接传入虚拟键值而不需要构造1-tuple，算是提供一点便捷。
			- 钩子启动时初始状态总为0。

			例如传入的statusTrnas为[(0,HookConstants.WM_LBUTTONDOWN,1),(1,HookConstants.WM_LBUTTONUP,0)]，
			那么在鼠标左键按下时状态切为1，左键抬起后切换为0。
		'''
		super().__init__(None,self.__KeyboardHook)
		self.__status=0
		self.__trans={}
		self.__callback={}
		for trans in statusTrans:
			oldStatus,key,newStatus=trans
			if(isinstance(key,list)):
				key=tuple(key)
			if(not isinstance(key,tuple)):
				key=(key,)
			elif(len(key)>1):
				key=(key[0],bool(key[1]))#用于防狗
			self.__trans.setdefault(oldStatus,[]).append((key,newStatus))
	def Opt_Start(self):
		self.__status=0
		super().Opt_Start()
	def Set_Callback(self,callback:dict={}):
		'''
			- callback格式为{status:func}，
				含义为：当进入到新状态时，会调用对应的回调函数func(MouseEvent)。
		'''
		self.__callback=callback
	def Get_Status(self):
		'''
			获取当前状态值
		'''
		return self.__status
	def __KeyboardHook(self,event:KeyboardEvent):
		if(self.__status in self.__trans):
			key=event.KeyID
			release=bool(event.IsTransition())
			for trans in self.__trans[self.__status]:
				condition,status=trans
				if(key==condition[0]):
					if(len(condition)==1 or not(condition[1]^release)):
						self.__status=status
						if(status in self.__callback):
							self.__callback[status](event)
						break
		return True





