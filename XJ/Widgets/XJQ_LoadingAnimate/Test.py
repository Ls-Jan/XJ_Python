
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_LoadingAnimate import XJQ_LoadingAnimate

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget,QListView,QHBoxLayout,QLabel,QPushButton


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		la=XJQ_LoadingAnimate()
		la.Set_Icon(size=QSize(64,64))
		self.__la=la
	def Opt_Run(self):
		self.__la.show()
		self.__la.resize(500,300)
		return super().Opt_Run()








