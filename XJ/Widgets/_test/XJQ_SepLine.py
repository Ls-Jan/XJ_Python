
from ..XJQ_SepLine import *

from PyQt5.QtWidgets import QApplication,QLabel,QGridLayout,QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

if True:
	app=QApplication([])

	win=QWidget()
	grid=QGridLayout(win)
	sep=XJQ_SepLine(Qt.Vertical,3,(50,0),QColor(0,0,192,192),Qt.DashDotLine)
	lbA=QLabel("AAA")
	lbB=QLabel("BBB")
	lbC=QLabel("CCC")
	lbD=QLabel("DDD")
	grid.addWidget(lbA,0,0)
	grid.addWidget(lbB,1,0)
	grid.addWidget(lbC,3,0)
	grid.addWidget(lbD,4,0)
	grid.addWidget(sep,2,0)

	win.show()
	win.resize(300,300)
	app.exec()



