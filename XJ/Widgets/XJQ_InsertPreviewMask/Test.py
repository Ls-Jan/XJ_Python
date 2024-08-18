__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from PyQt5.QtGui import QMouseEvent
from .XJQ_InsertPreviewMask import XJQ_InsertPreviewMask
from ...ModuleTest import XJQ_Test
from ...Functions.GetRealPath import GetRealPath
from ..XJQ_PureColorIcon import XJQ_PureColorIcon

class Win(QWidget):
	def __init__(self):
		super().__init__()
		msk=XJQ_InsertPreviewMask(self)
		msk.Set_UpArrowPict(XJQ_PureColorIcon(GetRealPath('箭头-010.png')).pixmap(64,64))
		msk.Set_ExcludeWidgets(self)
		msk.Set_IncludeLayout(QVBoxLayout(self))
		msk.Set_ValidDire(False,True)
		msk.hide()
		self.__msk=msk
	def mousePressEvent(self, event: QMouseEvent) -> None:
		self.__msk.show()
	def mouseMoveEvent(self, event: QMouseEvent) -> None:
		self.__msk.update()
		return super().mouseMoveEvent(event)
	def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
		self.__msk.hide()
		return super().mouseReleaseEvent(a0)


class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=Win()
		vbox=win.layout()
		for i in range(3):
			btn=QLabel()
			btn.setText(str(i))
			vbox.addWidget(btn)
		win.setAcceptDrops(True)
		self.__win=win
	def Opt_Run(self):
		self.__win.resize(640,480)
		self.__win.show()
		super().Opt_Run()
		# return self.__win






