
import sys
from PyQt5.QtWidgets import QApplication,QLabel,QWidget,QVBoxLayout

from ..XJQ_Tag import *

if True:
	app = QApplication(sys.argv)

	win=QWidget()
	win.show()

	vbox=QVBoxLayout(win)
	for style in [
			XJQ_Tag.Style.Blue,
			XJQ_Tag.Style.Gray,
			XJQ_Tag.Style.Orange,
			XJQ_Tag.Style.Red,
			XJQ_Tag.Style.Green,
			]:
		tag=XJQ_Tag(win,style.name,style)
		vbox.addWidget(tag)
		tag.show()
	win.setStyleSheet('background:rgb(20,20,20)')
	sys.exit(app.exec_())

