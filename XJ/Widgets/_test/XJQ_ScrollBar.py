
from ..XJQ_ScrollBar import *

import sys
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt

if True:
	app = QApplication(sys.argv)

	sb=XJQ_ScrollBar()
	# sb.setOrientation(Qt.Horizontal)
	sb.valueChanged.connect(lambda value:print(value))
	sb.setInvertedControls(False)#看我找到了什么？
	sb.setInvertedAppearance(True)#看我找到了什么？
	sb.setMaximum(50)
	# sb.setMaximum(5)
	sb.setValue(25)
	# sb.Set_Radius(15)
	# sb.setPageStep(1)

	win=QWidget()
	win.resize(700,400)
	win.show()
	win.setStyleSheet('background:#222222')
	vbox=QVBoxLayout(win)
	vbox.addWidget(sb)

	sys.exit(app.exec())

