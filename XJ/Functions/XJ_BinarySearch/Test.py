__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .XJ_BinarySearch import XJ_BinarySearch


__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		cnt=3 #lst长度
		lst=list(range(0,cnt<<1,2))

		for inv in [False,True]:
			if(inv):
				lst.reverse()
			print(">>>",lst)
			for val in range(-1,cnt<<1):
				print(f'[{val}]' if val%2==0 else f' {val} ',XJ_BinarySearch(lst,val,inv))
			print('\n\n')
		return super().Opt_Run()


