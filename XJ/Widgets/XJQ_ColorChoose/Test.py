
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_ColorChoose import XJQ_ColorChoose

from PyQt5.QtWidgets import QWidget

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		win=QWidget()
		cc=XJQ_ColorChoose(win)
		cc.setGeometry(100,100,200,100)
		cc.show()
		cc.Set_Color((128,64,32))
		cc.valueChanged.connect(lambda t:print(t))

		self.__win=win
	def Opt_Run(self):
		self.__win.resize(400,300)
		self.__win.show()
		super().Opt_Run()
		return self.__win







