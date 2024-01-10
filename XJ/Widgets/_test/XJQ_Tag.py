from ..XJQ_Tag import *

import sys
from PyQt5.QtWidgets import QApplication,QLabel,QWidget,QVBoxLayout

if True:
	app = QApplication(sys.argv)

	win=QWidget()
	win.show()

	vbox=QVBoxLayout(win)

	clickTest=False
	index=0
	for style in [
			XJQ_Tag.Style.Blue,
			XJQ_Tag.Style.Gray,
			XJQ_Tag.Style.Orange,
			XJQ_Tag.Style.Red,
			XJQ_Tag.Style.Green,
			]:
		tag=XJQ_Tag(win,style.name,style,clickable=clickTest or index%2==0)
		tag.clicked.connect(lambda val:print(val))
		vbox.addWidget(tag)
		index+=1
		tag.show()
	win.setStyleSheet('background:rgb(20,20,20)')
	sys.exit(app.exec_())

