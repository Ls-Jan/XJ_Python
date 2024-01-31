
import sys
from ..XJQ_ScrollBar import *
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt

if True:
	app = QApplication(sys.argv)

	slider=XJQ_ScrollBar()
	slider.setOrientation(Qt.Horizontal)
	slider.valueChanged.connect(lambda value:print(value))
	slider.setInvertedControls(False)#看我找到了什么？
	# slider.setInvertedAppearance(True)#看我找到了什么？
	slider.setMaximum(50)
	# slider.setMaximum(5)
	slider.setValue(25)

	win=QWidget()
	win.resize(700,400)
	win.show()
	vbox=QVBoxLayout(win)
	vbox.addWidget(slider)

	sys.exit(app.exec())

