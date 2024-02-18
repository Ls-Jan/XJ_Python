
from ..XJQ_SwitchBtn import *
from ...Functions.GetRealPath import *

from PyQt5.QtWidgets import QApplication,QPushButton,QWidget,QLabel,QHBoxLayout
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon

if True:
	app = QApplication([])

	win=QWidget()
	win.setStyleSheet('background:#222222;')
	win.resize(400,200)
	win.show()

	sb1=XJQ_SwitchBtn()
	sb1.valueChanged.connect(lambda flag:print(flag))
	sb2=XJQ_SwitchBtn(QPushButton(QIcon(GetRealPath('../icons/关闭.png')),'关闭'),QPushButton(QIcon(GetRealPath('../icons/打开.png')),'开启'))
	sb2.valueChanged.connect(lambda flag:print(flag))
	hbox=QHBoxLayout(win)
	hbox.addWidget(sb1)
	hbox.addWidget(sb2)
	app.exec_()
