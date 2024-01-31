

from ..XJQ_LoadingMask import *
from ...Functions import GetRealPath

import os
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout

if True:
	app = QApplication(sys.argv)

	# path=GetRealPath('../icons/上传.png')
	path=GetRealPath('../icons/加载动画-1.gif')

	win=QWidget()
	wid=XJQ_LoadingMask(path)
	wid.setParent(win)

	lb=QLabel("TEST")
	vbox=QVBoxLayout(win)
	vbox.addWidget(lb)
	win.show()
	win.resize(200,300)

	sys.exit(app.exec_())



