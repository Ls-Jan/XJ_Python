
from ..XJQ_SwitchBtn import *

from PyQt5.QtWidgets import QApplication,QPushButton,QWidget,QLabel,QHBoxLayout
from PyQt5.QtCore import QRect
from ...Functions import GetRealPath
if True:
	app = QApplication([])

	win=QWidget()
	win.setStyleSheet('background:#222222;')
	win.resize(400,200)
	win.show()

	sb1=XJQ_SwitchBtn()
	sb1.valueChanged.connect(lambda flag:print(flag))
	sb2=XJQ_SwitchBtn(GetRealPath('../icons/关闭.png'),GetRealPath('../icons/打开.png'))
	sb2.valueChanged.connect(lambda flag:print(flag))
	hbox=QHBoxLayout(win)
	hbox.addWidget(sb1)
	hbox.addWidget(sb2)

	app.exec_()
