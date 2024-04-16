
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from ..XJQ_SearchBox import XJQ_SearchBox

from PyQt5.QtWidgets import QWidget,QHBoxLayout
from PyQt5.QtCore import Qt

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		sb=XJQ_SearchBox()
		win=QWidget()
		self.__win=win
		self.__sb=sb

		sb.Set_StandbyList([f'{i}' for i in range(1000)],Qt.MatchFlag.MatchStartsWith)
		sb.commited.connect(lambda tx:print(f">>>>>>[{tx}]"))
		sb.Set_Size(18)
		print('尝试输入数字')
		# sb.updated.connect(lambda tx:sb.Set_StandbyList(['aaa','aab']))
		# sb.show()

		hbox=QHBoxLayout(win)
		hbox.addWidget(sb)
	def Opt_Run(self):
		self.__win.show()
		self.__sb.Set_Focus()
		super().Opt_Run()
		return self.__win







