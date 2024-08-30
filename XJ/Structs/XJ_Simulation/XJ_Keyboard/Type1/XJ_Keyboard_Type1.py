
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_Keyboard_Type1']

from ..VirtualKey import VirtualKey
from typing import Union
from pykeyboard import PyKeyboard

class XJ_Keyboard_Type1:
	'''
		有不同的方式实现键盘模拟：https://geek-docs.com/python/python-ask-answer/317_python_python_simulate_keydown.html。
		这里使用的是pykeyboard模块
	'''
	def __init__(self):
		self.__kb=PyKeyboard()
	def Opt_PressKey(self,key:Union[str,VirtualKey],Press:bool=True):
		kb=self.__kb
		if(isinstance(key,VirtualKey)):
			if(key==VirtualKey.Alt):
				key=kb.alt_key
			elif(key==VirtualKey.Back):
				key=kb.backspace_key
			elif(key==VirtualKey.Ctrl):
				key=kb.control_key
			elif(key==VirtualKey.Enter):
				key=kb.return_key
			elif(key==VirtualKey.Esc):
				key=kb.escape_key
			elif(key==VirtualKey.Tab):
				key=kb.tab_key
			elif(key==VirtualKey.Down):
				key=kb.down_key
			elif(key==VirtualKey.Right):
				key=kb.right_key
			elif(key==VirtualKey.Up):
				key=kb.up_key
			elif(key==VirtualKey.Left):
				key=kb.left_key
			elif(key==VirtualKey.Shift):
				key=kb.shift_key
			elif(key==VirtualKey.F1):
				key=kb.function_keys[1]
			elif(key==VirtualKey.F2):
				key=kb.function_keys[2]
			elif(key==VirtualKey.F3):
				key=kb.function_keys[3]
			elif(key==VirtualKey.F4):
				key=kb.function_keys[4]
			elif(key==VirtualKey.F5):
				key=kb.function_keys[5]
			elif(key==VirtualKey.F6):
				key=kb.function_keys[6]
			elif(key==VirtualKey.F7):
				key=kb.function_keys[7]
			elif(key==VirtualKey.F8):
				key=kb.function_keys[8]
			elif(key==VirtualKey.F9):
				key=kb.function_keys[9]
			elif(key==VirtualKey.F10):
				key=kb.function_keys[10]
			elif(key==VirtualKey.F11):
				key=kb.function_keys[11]
			elif(key==VirtualKey.F12):
				key=kb.function_keys[12]
			else:
				return
		if(Press):
			kb.press_key(key)
		else:
			kb.release_key(key)
	def Opt_TypeStr(self,string:str,ms:int):
		self.__kb.type_string(string,ms)




