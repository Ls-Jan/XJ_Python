from ..XJQ_Clock import *

from PyQt5.QtWidgets import QApplication,QPushButton,QWidget,QLabel
from PyQt5.QtCore import QRect

if True:
	app = QApplication([])

	ck=XJQ_Clock()
	ck.Opt_Continue(True)
	ck.show()

	app.exec_()


