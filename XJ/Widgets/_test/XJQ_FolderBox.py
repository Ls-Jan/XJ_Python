from PyQt5.QtWidgets import QApplication,QPushButton,QBoxLayout,QVBoxLayout,QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize

from ..XJQ_FolderBox import *
from ..XJQ_ListView import *
from ...Function import GetRealPath

if True:
	app = QApplication([])

	# lv=XJQ_ListView()
	wid=QWidget()
	vbox=QVBoxLayout(wid)
	for item in [
			('列表1',('A','B','C')),
			('列表2',('X','Y','Z')),]:
		fb=XJQ_FolderBox(item[0])
		fb.Set_Icon(QPixmap(GetRealPath("../icons/下箭头.png")),QPixmap(GetRealPath("../icons/上箭头.png")),size=QSize(24,24))
		# fbi=XJQ_FolderBox("列表",QBoxLayout.LeftToRight)
		# fbi.Set_Icon(QPixmap(GetRealPath("../icons/右箭头.png")),QPixmap(GetRealPath("../icons/左箭头.png")),size=QSize(32,32))
		fb.Set_Expand(True)
		vbox.addWidget(fb)
		# lv.Opt_AppendWidget(fb)
		cont=fb.Get_Content()
		cont.setStyleSheet('.QWidget{background:rgba(0,128,128,128)}')
		contBox=QVBoxLayout(cont)
		for val in item[1]:
			contBox.addWidget(QPushButton(val))
	vbox.addStretch(1)
	wid.show()
	# lv.show()
	app.exec_()

