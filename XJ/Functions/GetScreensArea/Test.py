__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .GetScreensArea import GetScreensArea
from PyQt5.QtWidgets import QPushButton,QSizePolicy


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		btn=QPushButton("获取本控件所在分屏的分辨率")
		# btn.clicked.connect(lambda:print(GetScreensArea(joint=True)))
		btn.clicked.connect(lambda:print(GetScreensArea(includeCursor=True)))
		self.__btn=btn
	def Opt_Run(self):
		self.__btn.resize(300,200)
		self.__btn.show()
		self.__btn.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		super().Opt_Run()
		return self.__btn






