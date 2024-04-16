
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_Clock import XJQ_Clock

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		ck=XJQ_Clock()
		ck.Opt_Continue(True)
		self.__ck=ck

	def Opt_Run(self):
		self.__ck.show()
		super().Opt_Run()
		# return self.__ck







