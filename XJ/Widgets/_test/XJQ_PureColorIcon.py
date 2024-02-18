
from ..XJQ_PureColorIcon import *
from ...Functions.GetRealPath import *

import os
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QLabel
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QCursor,QIcon

if True:
	app = QApplication(sys.argv)

	path=GetRealPath('../icons/V左箭头.png')
	# icon=XJQ_PureColorIcon(QIcon())
	icon=XJQ_PureColorIcon(path)
	icon.Set_Color(fg=(0,0,255,192))

	btn=QPushButton("ABC")
	btn.setIconSize(QSize(100,100))
	btn.setIcon(icon)
	
	btn.setStyleSheet('font-size:50px;')
	btn.show()
	btn.setStyleSheet('font-size:50px;color:#FFFF00;background:#FF8844')
	icon.Set_Color(wid=btn)#根据控件设置icon颜色(在控件显示后控件样式表才会应用生效于调色板中)
	btn.setIcon(icon)#发生变化的icon需要重新调用wid.setIcon(icon)才能生效
	btn.setCursor(QCursor(Qt.ForbiddenCursor))
	# btn.setCursor(QCursor(Qt.PointingHandCursor))

	s=QSize(260,160)
	s=s.boundedTo(s.transposed())
	btn.resize(s)
	btn.setIconSize(btn.size())
	print(btn.iconSize())
	btn.setText('')

	sys.exit(app.exec_())

