
from ..XJQ_PopupBox import *

from PyQt5.QtWidgets import QApplication,QPushButton,QHBoxLayout,QLabel,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt

if True:
	app = QApplication([])

	win=QWidget()
	win.setFocusPolicy(Qt.ClickFocus)
	win.show()
	# win.resize(900,700)
	win.setStyleSheet('.QWidget{background:rgb(164,192,255)}')
	win.resize(400,300)
	btn=QPushButton('ABC',win)
	btn.setGeometry(150,150,100,50)
	btn.show()

	wid=QWidget()
	wid.setStyleSheet('.QWidget{background:transparent}')
	vbox=QVBoxLayout(wid)
	for i in range(3):
		vbox.addWidget(QPushButton(str(i)*3))

	pbox=XJQ_PopupBox(btn)#弹窗，指向目标
	# pbox=XJQ_PopupBox(btn,arrowLength=20,arrowWidth=20)
	# pbox=XJQ_PopupBox(btn,arrowLength=100,arrowWidth=50)
	btn.clicked.connect(lambda:pbox.show())
	pbox.Set_Content(wid)#设置容器
	pbox.resize(None)
	pbox.show(True)

	app.exec_()


