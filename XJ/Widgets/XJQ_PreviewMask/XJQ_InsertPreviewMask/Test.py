__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from PyQt5.QtGui import QMouseEvent
from .XJQ_InsertPreviewMask import XJQ_InsertPreviewMask
from ....ModuleTest import XJQ_Test
from ....Functions.GetRealPath import GetRealPath
from ...XJQ_PureColorIcon import XJQ_PureColorIcon

class Win(QWidget):
	def __init__(self):
		super().__init__()
		vboxMain=QVBoxLayout(self)
		msk=XJQ_InsertPreviewMask(self)

		# for i in range(0):
		for i in range(2):
			btn=QLabel()
			btn.setText(str(i))
			btn.setMouseTracking(True)
			vboxMain.addWidget(btn)
		msk.Set_UpArrowPict(XJQ_PureColorIcon(GetRealPath('箭头-010.png')).pixmap(64,64))
		msk.Set_IncludeLayout(vboxMain)
		msk.Set_ValidDire(False,True)
		msk.hide()
		self.__msk=msk
		self.setMouseTracking(True)
	def enterEvent(self,event):
		self.__msk.show()
	def leaveEvent(self,event):
		self.__msk.hide()
	def mouseMoveEvent(self, event: QMouseEvent) -> None:
		self.__msk.update()
		return super().mouseMoveEvent(event)
	def mousePressEvent(self,event):
		print(self.__msk.Get_InsertPos())

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=Win()
		self.__win=win
	def Opt_Run(self):
		print("左键移动查看蒙版效果，左键点击获取插入点位置")
		self.__win.resize(640,480)
		self.__win.show()
		super().Opt_Run()
		# return self.__win






