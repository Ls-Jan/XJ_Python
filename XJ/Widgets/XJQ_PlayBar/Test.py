
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_PlayBar import XJQ_PlayBar

from PyQt5.QtWidgets import QWidget,QVBoxLayout

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		pb=XJQ_PlayBar()
		lst=[99,5,1,0,-1]#测试值
		# pb.Set_Index(0,lst[-1])
		# pb.Set_Index(0,lst[1])
		pb.Set_Index(0,lst[0])

		win=QWidget()
		vbox=QVBoxLayout(win)
		vbox.addWidget(pb)

		self.__win=win
	def Opt_Run(self):
		self.__win.resize(600,75)
		self.__win.show()
		return super().Opt_Run()





