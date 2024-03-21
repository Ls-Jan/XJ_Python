from ..CalcPopupArea import *
from ..GetScreensArea import *

from PyQt5.QtWidgets import QApplication,QPushButton,QMenu,QWidgetAction
from PyQt5.QtCore import QEvent, QTimerEvent, Qt,QSize,QPoint,QRect,pyqtSignal
from PyQt5.QtGui import QCursor, QFocusEvent, QShowEvent

if True:
	app=QApplication([])
	btn=QPushButton('左键点击弹出菜单')
	menu=QMenu(btn)
	menu.addAction('选项1')
	menu.addAction('选项2')
	menu.addAction('选项3')

	#QMenu支持自定义菜单：https://blog.csdn.net/Black_zy/article/details/116236766
	action=QWidgetAction(menu)
	action.setDefaultWidget(QPushButton("自定义菜单"))
	menu.addAction(action)
	def ShowMenu():
		pos=QCursor().pos()
		# menu.popup(pos)#其实QMenu有自带的弹出功能，不必用户去计算位置

		area=GetScreensArea(includeCursor=True)
		rst=CalcPopupArea(pos,menu.sizeHint(),area,0,True,True)
		print(pos,rst)
		if(rst):
			menu.setGeometry(rst[2])
		menu.show()
	btn.clicked.connect(ShowMenu)

	btn.show()
	btn.resize(600,300)
	btn.clicked.connect(ShowMenu)
	exit(app.exec())


