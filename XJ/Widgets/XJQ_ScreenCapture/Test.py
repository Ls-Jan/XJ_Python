__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from PyQt5.QtWidgets import QWidget,QLabel
from .XJQ_ScreenCapture import XJQ_ScreenCapture
from ...ModuleTest import XJQ_Test

from PyQt5.QtWidgets import QHBoxLayout,QLabel
class Win(QWidget):
	def __init__(self):
		super().__init__()
		lb=QLabel()
		sc=XJQ_ScreenCapture()
		sc.captured.connect(lambda pix:lb.setPixmap(pix))
		hbox=QHBoxLayout(self)
		hbox.addWidget(sc)
		hbox.addWidget(lb,1)
		self.__sc=sc
		self.__lb=lb


class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=Win()
		self.__win=win
	def Opt_Run(self):
		self.__win.resize(640,480)
		self.__win.show()
		super().Opt_Run()
		return self.__win






