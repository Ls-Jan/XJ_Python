
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_CanvasBox import XJQ_CanvasBox

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QRect

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		print('缩放以及拖拽时有明显的问题，有空一定修[doge]')
		cv= XJQ_CanvasBox()

		b=QPushButton('Test')
		b.setGeometry(QRect(10,10,100,100))
		b.clicked.connect(lambda:print("CLICK!!!"))

		b.setParent(cv)
		b.show()
		cv.Opt_MoveCenter(b,True)

		self.__cv=cv
	def Opt_Run(self):
		self.__cv.resize(800,500)
		self.__cv.show()
		super().Opt_Run()
		return self.__cv






