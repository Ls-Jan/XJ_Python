__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_Keyboard_Base']

from .VirtualKey import VirtualKey
from typing import Union
from time import sleep

class XJ_Keyboard_Base:
	'''
		键盘接口类。
		这是个抽象接口类，不直接使用，具体功能由派生类完成。
	'''
	def __init__(self):
		pass
	def Opt_Click(self,key:int,pressSecond:int=0.05):
		'''
			完成1次按键行为。
			pressSecond为鼠标按下与抬起之间的间隔。
			key的参数说明见Opt_PressKey。

		'''
		self.Opt_PressKey(key,True)
		sleep(pressSecond)
		self.Opt_PressKey(key,False)
	def Opt_PressKey(self,key:Union[str,VirtualKey],Press:bool=True):
		'''
			模拟按键按下/抬起。
			只允许ASCII单字符(非控制)、VirtualKey虚拟按键。
		'''
		pass
	def Opt_TypeStr(self,string:str,ms:int):
		'''
			指定时间内模拟输入一段字符串
		'''
		pass


