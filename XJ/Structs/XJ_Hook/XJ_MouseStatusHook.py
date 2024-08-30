__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_MouseStatusHook']

from .XJ_GlobalHook import XJ_GlobalHook
from PyHook3 import MouseEvent

class XJ_MouseStatusHook(XJ_GlobalHook):
	'''
		鼠标钩子。
		是XJ_GlobalHook的特化，额外封装了状态转换功能。
	'''
	def __init__(self,*statusTrans:tuple,callback:dict={}):
		'''
			- statusTrnas格式为(oldStatus,key,newStatus)，
				含义为：在旧状态oldStatus下，如果MouseEvent.Message的值与key相等，那么将进入到新状态newStatus。
			- callback格式为{status:func}，
				含义为：当进入到新状态时，会调用对应的回调函数func()。
			- 钩子启动时初始状态总为0。

			例如传入的statusTrnas为[(0,HookConstants.WM_LBUTTONDOWN,1),(1,HookConstants.WM_LBUTTONUP,0)]，
			那么在鼠标左键按下时状态切为1，左键抬起后切换为0。
		'''
		super().__init__(self.__MouseHook,None)
		self.__status=0
		self.__trans={}
		self.__callback=callback
		for trans in statusTrans:
			self.__trans.setdefault(trans[0],[]).append(trans[1:])
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
	def __MouseHook(self,event:MouseEvent):
		if(self.__status in self.__trans):
			msg=event.Message
			for trans in self.__trans[self.__status]:
				key,status=trans
				if(msg==key):
					self.__status=status
					if(status in self.__callback):
						self.__callback[status](event)
					break
		return True


