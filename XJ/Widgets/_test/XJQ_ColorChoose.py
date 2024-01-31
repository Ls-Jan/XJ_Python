
from ..XJQ_ColorChoose import *

import sys
from PyQt5.QtWidgets import QApplication,QWidget

if True:
	app = QApplication(sys.argv)

	win=QWidget()
	win.resize(400,300)
	win.show()

	test=XJQ_ColorChoose(win)
	test.setGeometry(100,100,200,100)
	test.show()
	test.Set_Color((128,64,32))
	test.valueChanged.connect(lambda t:print(t))

	sys.exit(app.exec())


