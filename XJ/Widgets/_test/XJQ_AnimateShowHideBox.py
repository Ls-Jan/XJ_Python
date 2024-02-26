
from ..XJQ_AnimateShowHideBox import *

from PyQt5.QtWidgets import QApplication,QPushButton,QWidget
from PyQt5.QtCore import QRect,Qt
from PyQt5.QtGui import QLinearGradient

if True:
	app = QApplication([])

	win=QWidget()
	win.resize(400,200)

	btn=QPushButton("Test",win)
	btn.clicked.connect(lambda:print("TEST"))

	shbox=XJQ_AnimateShowHideBox(win)
	shbox.setGeometry(QRect(0,50,100,50))
	shbox.Set_Content(btn)
	shbox.Set_Duration(1000)
	
	show=QPushButton("Show",win)
	show.setGeometry(QRect(150,50,100,50))
	show.clicked.connect(lambda:shbox.show(autoHide=100))

	hide=QPushButton("Hide",win)
	hide.setGeometry(QRect(150,100,100,50))
	hide.clicked.connect(lambda:shbox.hide())

	# lg=QLinearGradient(0,0,btn.size().width(),btn.size().height())
	# lg.setColorAt(0.0,Qt.transparent)
	# lg.setColorAt(0.5,Qt.black)
	# lg.setColorAt(1.0,Qt.transparent)
	# QGraphicsOpacityEffect.setOpacityMask(lg)

	win.show()
	app.exec_()




