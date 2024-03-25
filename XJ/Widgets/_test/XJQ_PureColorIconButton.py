from ..XJQ_PureColorIconButton import XJQ_PureColorIconButton
from ..XJQ_PureColorIcon import XJQ_PureColorIcon
from ...Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QApplication,QWidget,QStackedLayout

if True:
	app=QApplication([])
	win=QWidget()
	win.show()
	win.resize(300,300)
	ib=XJQ_PureColorIconButton(XJQ_PureColorIcon(GetRealPath('../../Icons/停止.png')),win)
	ib.clicked.connect(lambda:print("CLICK"))
	ib.resize(200,200)
	print('暂不清楚为什么sizeHint影响了窗口的最小大小，可能是sizeHint导致的，也可能是栈布局QStackedLayout造成的')
	stk=QStackedLayout(win)
	stk.addWidget(ib)
	win.setStyleSheet('background:#222222;')

	app.exec_()
