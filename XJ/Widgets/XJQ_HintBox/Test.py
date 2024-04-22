
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_HintBox import XJQ_HintBox

from PyQt5.QtWidgets import QWidget,QListView,QHBoxLayout,QLabel,QPushButton,QSizePolicy


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		tp=QPushButton("弹窗按钮")
		tp.resize(100,50)

		hibox=XJQ_HintBox()
		hibox.Set_Content(tp)
		hibox.hide()
		# hibox.Set_AutoHide(True)

		win=QPushButton("点击本按钮查看效果\n弹窗会与鼠标保持一定距离")
		win.clicked.connect(lambda:hibox.update())
		win.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding))
		self.__win=win
	def Opt_Run(self):
		self.__win.resize(500,300)
		self.__win.show()
		super().Opt_Run()
		return self.__win








