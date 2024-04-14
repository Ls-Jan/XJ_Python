
__version__='1.0.0'
__author__='Ls_Jan'

from .XJ_Test import XJ_Test
from PyQt5.QtWidgets import QApplication

__all__=['XJQ_Test']

class XJQ_Test(XJ_Test):
	'''
		继承XJ_Test的泛型，特用于Widgets模块的控件测试。

		Opt_Run需要重写，并主动调用控件的show函数
	'''
	def __init__(self):
		super().__init__()
		app=QApplication.instance()
		self.__app=None
		if(app==None):
			self.__app=QApplication([])
	def Opt_Run(self):
		if(self.__app):
			self.__app.exec()


