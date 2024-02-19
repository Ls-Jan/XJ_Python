
from ..XJ_MouseStatus import *


import sys
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt


class Test(QWidget):
	__mouseStatus=None
	def __init__(self,*arg):
		super().__init__(*arg)
		ms=XJ_MouseStatus()
		ms.longClick.connect(lambda:print("<LongClick!>"))
		self.__mouseStatus=ms
	def __EasyPrint(self):
		press={
			QMouseEvent.MouseButtonRelease:"Release",
			QMouseEvent.MouseButtonPress:"Press",
			QMouseEvent.MouseButtonDblClick:"DblClick",}
		button={
			Qt.LeftButton:'Left',
			Qt.MidButton:'Middle',
			Qt.RightButton:'Right',}
		tPoint=lambda point:(point.x(),point.y())
		tBtn=lambda btn:[button[key] for key in button if key&btn]
		tBtnStatus=lambda status:(tBtn(status[0]),press[status[1]])

		ms=self.__mouseStatus
		pos=tPoint(self.mapFromGlobal(ms.Get_Position()))
		moveDelta=tPoint(ms.Get_MoveDelta())
		btnStatus=tBtnStatus(ms.Get_PressButtonStatus())
		print(f'pos{pos},\tdelta{moveDelta},\t{btnStatus[0]}-{btnStatus[1]}')
		if(btnStatus[1]=='Release'):
			print()
	def mousePressEvent(self,event):
		self.__mouseStatus.Opt_Update(event)
		self.__EasyPrint()
	def mouseMoveEvent(self,event):
		self.__mouseStatus.Opt_Update(event)
		self.__EasyPrint()
	def mouseReleaseEvent(self,event):
		self.__mouseStatus.Opt_Update(event)
		self.__EasyPrint()

if True:
	app = QApplication(sys.argv)

	t=Test()
	t.show()

	sys.exit(app.exec())

