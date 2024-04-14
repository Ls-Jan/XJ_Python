
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from ..XJQ_PureColorIconButton import XJQ_PureColorIconButton
from ..XJQ_PureColorIcon import XJQ_PureColorIcon
from ...Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QWidget,QStackedLayout

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=QWidget()
		ib=XJQ_PureColorIconButton(XJQ_PureColorIcon(GetRealPath('../../Icons/停止.png')),win)
		ib.clicked.connect(lambda:print("CLICK"))
		# print('暂不清楚为什么sizeHint影响了窗口的最小大小，可能是sizeHint导致的，也可能是栈布局QStackedLayout造成的')
		stk=QStackedLayout(win)
		stk.addWidget(ib)
		win.setStyleSheet('background:#222222;')
		win.resize(300,300)
		ib.resize(200,200)
		self.__win=win
	def Opt_Run(self):
		self.__win.show()
		return super().Opt_Run()



