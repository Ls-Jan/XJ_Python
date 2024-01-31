from ..XJQ_IconButton import *
from ..XJQ_Icon import *
from ...Functions.GetRealPath import *

from PyQt5.QtWidgets import QApplication,QWidget,QStackedLayout

if True:
	app=QApplication([])
	win=QWidget()
	win.show()
	win.resize(300,300)
	ib=XJQ_IconButton(GetRealPath('../icons/停止.png'),win)
	ib.clicked.connect(lambda:print("CLICK"))
	stk=QStackedLayout(win)
	stk.addWidget(ib)
	win.setStyleSheet('background:#222222;')

	app.exec_()
