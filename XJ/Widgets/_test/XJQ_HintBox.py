


from PyQt5.QtGui import QMouseEvent
from ..XJQ_HintBox import *

from PyQt5.QtWidgets import QApplication,QWidget,QListView,QHBoxLayout,QLabel,QPushButton


if True:
	app = QApplication([])

	tp=QPushButton("弹窗按钮")
	tp.show()

	hibox=XJQ_HintBox()
	hibox.update()
	hibox.Set_Content(tp)
	# hibox.Set_AutoHide(True)

	win=QPushButton("点击按钮查看效果")
	win.resize(500,300)
	win.show()
	win.clicked.connect(lambda:hibox.update())

	exit(app.exec_())
