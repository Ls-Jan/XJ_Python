
from ..XJQ_PureColorIcon import *
from ...Functions.GetRealPath import *

import os
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QLabel
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QCursor,QIcon

if True:
	app = QApplication(sys.argv)

	path=GetRealPath('../../Icons/云下载.png')
	# path=GetRealPath('../../Icons/Arrow/V左箭头.png')
	icon=XJQ_PureColorIcon(path,squareSize=False)
	icon.Set_Color(fg=(0,0,255,192))

	btn=QPushButton("ABC")	
	btn.setStyleSheet('font-size:50px;color:#FFFF00;background:#FF8844')
	btn.setIconSize(QSize(64,64))
	btn.setCursor(QCursor(Qt.ForbiddenCursor))
	# btn.setCursor(QCursor(Qt.PointingHandCursor))

	btn.show()
	btn.resize(200,btn.height())
	icon.Set_Color(wid=btn)#根据控件设置icon颜色(在控件显示后控件样式表才会应用生效于调色板中)。通过该方法设置图标颜色的效果有时不理想
	btn.setIcon(icon)#发生变化的icon需要重新调用wid.setIcon(icon)才能生效

	sys.exit(app.exec_())

