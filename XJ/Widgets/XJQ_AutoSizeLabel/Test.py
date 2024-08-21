
__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from ...ModuleTest import XJQ_Test
from .XJQ_AutoSizeLabel import XJQ_AutoSizeLabel

from PyQt5.QtGui import QMovie,QPixmap
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QLabel
from XJ.Functions.GetRealPath import GetRealPath

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		win=QWidget()
		hbox=QHBoxLayout(win)
		for i in range(2):
			lb=XJQ_AutoSizeLabel()
			pix=QPixmap(GetRealPath('图标-剪贴板.png')).scaled(128+64*i,128+64*i)
			lb.Set_PictResize(1+i)
			lb.setPixmap(pix)
			lb.setStyleSheet('background:#FF0000')
			hbox.addWidget(lb)
		self.__win=win
	def Opt_Run(self):
		self.__win.resize(320,160)
		self.__win.show()
		super().Opt_Run()



