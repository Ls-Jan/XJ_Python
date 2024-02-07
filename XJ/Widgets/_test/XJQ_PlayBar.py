from ..XJQ_PlayBar import *

from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout

if True:
	app = QApplication([])

	pb=XJQ_PlayBar()

	win=QWidget()
	win.resize(600,75)
	win.show()
	vbox=QVBoxLayout(win)
	vbox.addWidget(pb)

	app.exec_()

