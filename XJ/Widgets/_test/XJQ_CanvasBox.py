
from ..XJQ_CanvasBox import *

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton
from PyQt5.QtCore import QRect

if True:
	app = QApplication(sys.argv)

	cv= XJQ_CanvasBox()
	cv.show()
	cv.resize(800,500)

	b=QPushButton('Test')
	b.setGeometry(QRect(10,10,100,100))
	b.clicked.connect(lambda:print("CLICK!!!"))

	b.setParent(cv)
	b.show()
	cv.Opt_MoveCenter(b,True)

	sys.exit(app.exec())

