__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from .XJQ_ScreenAreaSelector import XJQ_ScreenAreaSelector
from ...ModuleTest import XJQ_Test

from PyQt5.QtWidgets import QVBoxLayout,QPushButton,QLabel
class Win(QWidget):
	def __init__(self):
		super().__init__()
		vbox=QVBoxLayout(self)
		lb=QLabel()
		btn=QPushButton("点击截图")
		sa=XJQ_ScreenAreaSelector()
		vbox.addWidget(lb,1)
		vbox.addWidget(btn)
		btn.clicked.connect(lambda:sa.show())
		sa.doubleClicked.connect(lambda :(lb.setPixmap(sa.Get_Screenshot()),sa.hide(),sa.Opt_Clear()))
		self.__sa=sa
		self.__lb=lb


class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=Win()
		self.__win=win
	def Opt_Run(self):
		self.__win.resize(640,480)
		self.__win.show()
		super().Opt_Run()
		return self.__win






