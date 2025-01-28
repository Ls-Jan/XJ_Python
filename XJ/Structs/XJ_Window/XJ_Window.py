__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_Window']

import win32con
import win32api
import win32gui
import win32process

class XJ_Window:
	'''
		将一些有关窗口的函数进行简单的封装
	'''
	def __init__(self,hwnd:int=0):
		'''
			hwnd未定时可通过两种方式进行修改：
				- 通过属性XJ_Window.hwnd直接赋值；
				- 通过XJ_Window.Set_Hwnd进行设置；
		'''
		self.__hwnd=hwnd
	@property
	def hwnd(self):
		return self.__hwnd
	@hwnd.setter
	def hwnd(self,hwnd:int):
		self.__hwnd=hwnd
	def Get_WinPos(self):
		'''
			获取窗口位置LTWH。
			特别的，如果句柄无效则返回None。

			假若出现返回数据与实际情况不一致，则需要调用XJ_Window.Set_DPIAawreness设置DPI动态感知
		'''
		hwnd=self.__hwnd
		rect=None
		if(win32gui.IsWindow(hwnd)):
			rect=list(win32gui.GetWindowRect(hwnd))
			for i in range(2):
				rect[i+2]-=rect[i]
		return rect
	def Get_IsValidHwnd(self):
		'''
			判断窗口句柄是否有效
		'''
		return win32gui.IsWindow(self.__hwnd)
	def Set_Hwnd(self,cursorPos:tuple=None,rootWin:bool=False,activeWin:bool=False):
		'''
			设置窗口句柄，会顺手返回窗口句柄。

			如果activeWin为真则返回当前活跃窗口，为假会根据cursorPos返回对应窗口，特别的，cursorPos为空则使用鼠标位置。
			如果rootWindow为真则会返回顶级父窗口的句柄。
		'''
		if(activeWin):
			hwnd=win32gui.GetForegroundWindow()
		else:
			if(cursorPos==None):
				cursorPos=win32api.GetCursorPos()
			hwnd=win32gui.WindowFromPoint(cursorPos)
			if(rootWin):
				tmp=hwnd
				while(tmp):
					hwnd=tmp
					tmp=win32gui.GetParent(tmp)
		self.__hwnd=hwnd
		return hwnd
	def Set_WinPos(self,pos:tuple=None,size:tuple=None):
		'''
			设置窗口位置以及窗口大小
		'''
		hwnd=self.__hwnd
		if(win32gui.IsWindow(hwnd)):
			flags=win32con.SWP_NOZORDER
			if(pos==None):
				pos=(0,0)
				flags|=win32con.SWP_NOMOVE
			if(size==None):
				size=(0,0)
				flags|=win32con.SWP_NOSIZE
			win32gui.SetWindowPos(hwnd,None,*pos,*size,flags)
	def Get_WinText(self):
		'''
			获取窗口标题
		'''
		win32gui.GetWindowText(self.__hwnd)
	def Get_WinThreadProcessId(self):
		'''
			获取窗口的tid以及pid，返回2-tuple
		'''
		return win32process.GetWindowThreadProcessId(self.__hwnd)
	@staticmethod
	def Set_DPIAawreness(thread:bool=True):
		'''
			windows专供(或者说win10专享)。
			将DPI模式设置为动态感知，以同步逻辑屏幕和物理屏幕。
			不同步的话很多API将会出现各种问题。
		'''
		from ctypes import CDLL
		user32=CDLL('user32.dll')
		flag=-3#这个值对应DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE
		if(thread):
			user32.SetThreadDpiAwarenessContext(flag)
		else:
			user32.SetProcessDpiAwarenessContext(flag)



