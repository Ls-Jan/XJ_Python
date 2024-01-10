# XJQ_MouseStatus

鼠标状态记录，不单独使用，只处理单键(多键行为请在外部代码控制)

用于简化mousePressEvent、mouseMoveEvent和mouseReleaseEvent的部分鼠标控制逻辑，

<br>

包括鼠标长按(防抖)、鼠标双击、鼠标拖拽移动量(相对和绝对)、鼠标位置、鼠标拖拽时的移动判断

可设置长按间隔、双击间隔、防抖距离(鼠标按下时移动量不超过该值时鼠标被视为未移动状态)


![XJQ_MouseStatus](../pict/XJQ_MouseStatus.gif)


```py
from XJ.Widgets import XJQ_MouseStatus

import sys
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt


class Test(QWidget):
	__mouseStatus=None
	def __init__(self,*arg):
		super().__init__(*arg)
		ms=XJQ_MouseStatus()
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
```
