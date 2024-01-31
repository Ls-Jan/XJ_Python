
from ..GrabScreen import *

from PyQt5.QtWidgets import QApplication,QLabel
import time

class Test(QLabel):
	def mousePressEvent(self,event):
		bTime=time.time()
		pix,rect=GrabScreen(0)
		# pix,rect=GrabScreen(-1)
		cTime=time.time()
		#平均用时50ms左右，不快不慢，适合截图但不适合录屏(20hz的帧率太低了)
		print(f'{int((cTime-bTime)*1000)}ms',pix,rect)
		pix=pix.scaled(self.size())
		self.setPixmap(pix)
		

if True:
	app = QApplication([])

	ck=Test('点击截图')
	ck.resize(1000,600)
	ck.show()

	app.exec_()




