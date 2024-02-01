from ..XJQ_Slider import *

import sys
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt

if True:
	app = QApplication(sys.argv)

	slider=XJQ_Slider()
	slider.setOrientation(Qt.Horizontal)
	slider.valueChanged.connect(lambda value:print(value))
	slider.setInvertedControls(False)#看我找到了什么？
	slider.setInvertedAppearance(False)#看我找到了什么？
	# slider.setInvertedControls(True)#看我找到了什么？
	# slider.setInvertedAppearance(True)#看我找到了什么？
	slider.setMaximum(50)
	# slider.setMaximum(5)
	slider.setValue(25)
	slider.setValue(extra=40)

	win=QWidget()
	win.resize(700,400)
	win.setStyleSheet('background:#222222')
	win.show()
	vbox=QVBoxLayout(win)
	vbox.addWidget(slider)

	sys.exit(app.exec())

