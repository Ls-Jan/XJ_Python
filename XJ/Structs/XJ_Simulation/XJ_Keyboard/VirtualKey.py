__version__='1.0.0'
__author__='Ls_Jan'
__all__=['VirtualKey']

from enum import IntEnum

class VirtualKey(IntEnum):
	'''
		记录一些常用的特殊按键，诸如：
			- 控制键：Ctrl、Shift、Alt、Tab、Enter、Esc、Backspace；
			- 功能键(F1~F12)；
			- 方向键(up/down/left/right)；

		以下枚举的具体数值实际上使用的是win32的虚拟键枚举值：https://learn.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes。
		虽然应该使用win32con.VK_XXX的，但还是算了。
	'''
	Back=0x08#退格键
	Tab=0x09
	Shift=0x10
	Ctrl=0x11
	Alt=0x12#其实是Menu
	Enter=13#其实是Return
	Esc=0x1B
	Left=0x25
	Up=0x26
	Right=0x27
	Down=0x28
	F1=0x70
	F2=0x71
	F3=0x72
	F4=0x73
	F5=0x74
	F6=0x75
	F7=0x76
	F8=0x77
	F9=0x78
	F10=0x79
	F11=0x7A
	F12=0x7B


