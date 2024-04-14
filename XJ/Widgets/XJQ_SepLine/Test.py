
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_SepLine import XJQ_SepLine

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGridLayout,QLabel,QWidget

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		win=QWidget()
		grid=QGridLayout(win)
		sep=XJQ_SepLine(Qt.Vertical,3,(50,0),QColor(0,0,192,192),Qt.DashDotLine)
		lbA=QLabel("AAA")
		lbB=QLabel("BBB")
		lbC=QLabel("CCC")
		lbD=QLabel("DDD")
		grid.addWidget(lbA,0,0)
		grid.addWidget(lbB,1,0)
		grid.addWidget(lbC,3,0)
		grid.addWidget(lbD,4,0)
		grid.addWidget(sep,2,0)
		
		self.__win=win
	def Opt_Run(self):
		self.__win.show()
		self.__win.resize(300,300)
		return super().Opt_Run()




