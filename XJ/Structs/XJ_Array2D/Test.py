__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .XJ_Array2D import XJ_Array2D


__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		b=XJ_Array2D()
		b[1,3]=6
		b[1,4]=8
		b[1,5]=10
		print(b)
		# print(b[1:4,5])
		# print(b[1:4,5:6])
		print(b[1:2,4:6])
		print(b[1,4:6])
		print()
		print(b.size())

		# for i in range(b.size()[0]):
			# print(b[i][3:5+1])
		return super().Opt_Run()


