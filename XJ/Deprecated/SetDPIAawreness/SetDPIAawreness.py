
__version__='1.0.0'
__author__='Ls_Jan'


__all__=['SetDPIAawreness']

def SetDPIAawreness(thread:bool=True):
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



