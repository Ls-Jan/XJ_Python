__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .GrabScreen import GrabScreen

from PyQt5.QtWidgets import QLabel
import time

class TestWidget(QLabel):
	def mousePressEvent(self,event):
		bTime=time.time()
		pix,rect=GrabScreen(0)
		# pix,rect=GrabScreen(-1)
		cTime=time.time()
		print(f'{int((cTime-bTime)*1000)}ms',pix,rect)
		pix=pix.scaled(self.size())
		self.setPixmap(pix)
		


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		self.__ck=TestWidget('点击截图')
		print('每个抓屏操作平均用时50ms左右，不快不慢，适合截图但不适合录屏(20hz的帧率太低了)')
	def Opt_Run(self):
		self.__ck.resize(1000,600)
		self.__ck.show()
		super().Opt_Run()
		return self.__ck










