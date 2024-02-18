from ..GetScreensArea import *

from PyQt5.QtWidgets import QApplication,QPushButton

if True:
	app = QApplication([])

	btn=QPushButton("Test")
	# btn.clicked.connect(lambda:print(GetScreensArea(joint=True)))
	btn.clicked.connect(lambda:print(GetScreensArea(includeCursor=True)))
	btn.resize(200,100)
	btn.show()

	app.exec_()

