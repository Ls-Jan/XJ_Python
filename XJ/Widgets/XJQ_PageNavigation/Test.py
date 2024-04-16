
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_PageNavigation import XJQ_PageNavigation


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		print('【该控件为半成品，将来会对其进行重构】')
		pn=XJQ_PageNavigation()
		pn.Set_DataCount(150)
		pn.Set_PerCountList([1,2,3,4,5,10,100])
		pn.changed.connect(lambda start,count:print(start,start+count-1))
		self.__pn=pn
	def Opt_Run(self):
		self.__pn.resize(250,50)
		self.__pn.show()
		super().Opt_Run()
		# return self.__pn




