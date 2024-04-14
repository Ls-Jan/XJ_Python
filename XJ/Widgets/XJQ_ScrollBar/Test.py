
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_ScrollBar import *

from PyQt5.QtWidgets import QVBoxLayout,QWidget

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		sb=XJQ_ScrollBar()
		# sb.setOrientation(Qt.Horizontal)
		sb.valueChanged.connect(lambda value:print(value))
		sb.setInvertedControls(False)#看我找到了什么？
		sb.setInvertedAppearance(True)#看我找到了什么？
		sb.setMaximum(50)
		# sb.setMaximum(5)
		sb.setValue(25)
		# sb.Set_Radius(15)
		# sb.setPageStep(1)

		win=QWidget()
		win.setStyleSheet('background:#222222')
		vbox=QVBoxLayout(win)
		vbox.addWidget(sb)
		self.__win=win
	def Opt_Run(self):
		self.__win.resize(700,400)
		self.__win.show()
		return super().Opt_Run()





