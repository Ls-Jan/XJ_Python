__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_Keyboard']

from .VirtualKey import VirtualKey
from typing import Union

class XJ_Keyboard:
	'''
		键盘接口类。
		这是个抽象接口类，不直接使用，具体功能由派生类完成。
	'''
	def __init__(self):
		pass
	def Opt_PressKey(self,key:Union[str,VirtualKey],Press:bool=True):
		'''
			模拟按键按下/抬起。
			只允许ASCII字符(非控制)、VirtualKey虚拟按键。
		'''
		pass
	def Opt_TypeStr(self,string:str,ms:int):
		'''
			指定时间内模拟输入一段字符串
		'''
		pass




