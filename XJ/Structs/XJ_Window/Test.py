__version__='1.0.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .XJ_Window import XJ_Window
from PyHook3 import HookConstants


__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		print('测试样例未完成')
		return super().Opt_Run()


