

from ..XJ_Mouse import XJ_Mouse
from pymouse import PyMouse

__all__=['XJ_Mouse_Type1']

class XJ_Mouse_Type1(XJ_Mouse):
	'''
		该派生类使用模块PyMouse实现鼠标控制。
		
		PyMouse模块安装(pip install的是PyUserInput而不是PyMouse)：https://github.com/pepijndevos/PyMouse
	'''
	def __init__(self):
		super().__init__()
		self.__ms=PyMouse()
	def Opt_PressKey(self,key:int,Press:bool=True):
		if(Press):
			self.__ms.press(*self.__ms.position(),key)
		else:
			self.__ms.release(*self.__ms.position(),key)
	def Opt_Wheel(self,delta:int,horizontal:bool=False):
		v,h=delta,0 if horizontal else 0,delta
		self.__ms.scroll(v,h)
	def Opt_Move(self,pos:tuple):
		self.__ms.move(*pos)
	def Get_Pos(self):
		return self.__ms.position()








