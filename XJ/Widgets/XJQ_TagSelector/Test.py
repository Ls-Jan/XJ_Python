
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_TagSelector import XJQ_TagSelector

from random import randint

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		ts=XJQ_TagSelector()

		# bit=1
		bit=3
		ts.selected.connect(lambda name,flag:print(name,flag))
		ts.setStyleSheet('.XJQ_TagSelector{background:#222222}')

		ts.Set_TagLst([oct(i)[2:].rjust(randint(1,10)) for i in range(8**bit)])
		# ts.Set_TagLst([oct(i)[2:].zfill(bit) for i in range(8**bit)])
		# ts.Set_TagLst([bin(i)[2:].zfill(7) for i in range(128)])
		# ts.Set_TagLst([str(i).zfill(3) for i in range(100)])
		self.__ts=ts
	def Opt_Run(self):
		self.__ts.show()
		self.__ts.resize(800,400)
		print('标签数量过多时，有时候会出现卡顿问题(暂未找到优化方案)')
		return super().Opt_Run()




