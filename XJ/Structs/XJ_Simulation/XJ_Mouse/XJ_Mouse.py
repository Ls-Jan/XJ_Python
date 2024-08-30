

__all__=['XJ_Mouse']

class XJ_Mouse:
	'''
		鼠标接口类。
		这是个抽象接口类，不直接使用，具体功能由派生类完成。

		特别说明，如果不使用PyQt5的话就得需要使用winAPI的SetThreadDpiAwarenessContext设置DPI动态感知，否则多数情况下鼠标移动会出现问题
	'''
	def __init__(self):
		pass
	def Opt_PressKey(self,key:int,Press:bool=True):
		'''
			模拟鼠标按下/抬起。
			key可选值为：左键(1)、右键(2)、中键(3)
		'''
		pass
	def Opt_Wheel(self,delta:int,horizontal:bool=False):
		'''
			模拟鼠标滚轮。
			delta为滚动量，为正时向下/右滚动，为负时向左/上滚动
		'''
		pass
	def Opt_Move(self,pos:tuple):
		'''
			移动鼠标到指定坐标。
		'''
		pass
	def Get_Pos(self):
		'''
			获取鼠标坐标，返回2-tuple。
		'''
		pass





