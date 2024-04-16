
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_PopupBox import XJQ_PopupBox

from PyQt5.QtWidgets import QPushButton,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		win=QWidget()
		win.setFocusPolicy(Qt.ClickFocus)
		win.setStyleSheet('.QWidget{background:rgb(164,192,255)}')
		win.resize(400,300)
		btn=QPushButton('试着调整窗口大小',win)
		btn.setGeometry(50,50,200,100)
		self.__win=win
		self.__btn=btn
	def Opt_Run(self):
		pbox=XJQ_PopupBox(self.__btn)#弹窗，指向目标
		# pbox=XJQ_PopupBox(btn,arrowLength=20,arrowWidth=20)
		# pbox=XJQ_PopupBox(btn,arrowLength=100,arrowWidth=50)
		wid=QWidget()
		wid.setStyleSheet('.QWidget{background:transparent}')
		vbox=QVBoxLayout(wid)
		for i in range(3):
			vbox.addWidget(QPushButton(str(i)*3))
		pbox.Set_Content(wid)#设置容器
		pbox.resize(None)
		pbox.show(True)
		self.__btn.clicked.connect(lambda:pbox.show())

		# win.resize(900,700)
		self.__win.show()
		super().Opt_Run()
		# return self.__win






