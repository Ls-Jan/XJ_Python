
__version__='1.1.0'
__author__='Ls_Jan'


from .XJQ_SwitchBtn import XJQ_SwitchBtn
from ..XJQ_PureColorIconButton import XJQ_PureColorIconButton
from ...Functions.GetRealPath import GetRealPath
from ...ModuleTest import XJQ_Test

from PyQt5.QtWidgets import QApplication,QPushButton,QWidget,QHBoxLayout
from PyQt5.QtGui import QIcon

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		win=QWidget()
		win.setStyleSheet('background:#222222;')
		sb1=XJQ_SwitchBtn(XJQ_PureColorIconButton(GetRealPath('./播放.png')),XJQ_PureColorIconButton(GetRealPath('./暂停.png')))
		sb1.valueChanged.connect(lambda flag:print(flag))
		sb2=XJQ_SwitchBtn(QPushButton(QIcon(GetRealPath('./关闭.png')),'关闭'),QPushButton(QIcon(GetRealPath('./打开.png')),'开启'))
		sb2.valueChanged.connect(lambda flag:print(flag))
		hbox=QHBoxLayout(win)
		hbox.addWidget(sb1)
		hbox.addWidget(sb2)

		self.__win=win
	def Opt_Run(self):
		self.__win.resize(400,200)
		self.__win.show()
		return super().Opt_Run()





