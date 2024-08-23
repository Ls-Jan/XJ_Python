__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from PyQt5.QtCore import Qt
from .XJQ_SelectedPreviewMask import XJQ_SelectedPreviewMask
from ....ModuleTest import XJQ_Test

class Win(QWidget):
	def __init__(self):
		super().__init__()
		msk=XJQ_SelectedPreviewMask(self)
		msk.show()
		self.__msk=msk
	def mousePressEvent(self,event):
		self.__msk.Opt_Press(bool(event.modifiers()&Qt.Modifier.CTRL))
	def mouseMoveEvent(self,event):
		self.__msk.Opt_Drag()
		print('拖拽控件：',[wid.objectName() for wid in self.__msk.Get_SelectedWidgets()])
		# self.__msk.Opt_Clear()
	def mouseReleaseEvent(self,event):
		self.__msk.Opt_Release()
		
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=Win()
		vbox=QVBoxLayout(win)
		for i in range(3):
			wid=QLabel(f'Box:{i}')
			wid.setObjectName(str(i))
			vbox.addWidget(wid)
		self.__win=win
	def Opt_Run(self):
		print("左键点击盒布局(右)内的QLabel")
		print("按下Ctrl点击可进行多选")
		self.__win.resize(640,240)
		self.__win.show()
		super().Opt_Run()
		return self.__win






