
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_FolderBox import XJQ_FolderBox
from ..XJQ_ListWidget import XJQ_ListWidget
from ...Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QPushButton,QBoxLayout,QVBoxLayout,QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		# lv=XJQ_ListView()
		print('【该控件为半成品，将来会对其进行重构】')
		wid=QWidget()
		vbox=QVBoxLayout(wid)
		for item in [
				('列表1',('A','B','C')),
				('列表2',('X','Y','Z')),]:
			fb=XJQ_FolderBox(item[0])
			fb.Set_Icon(QPixmap(GetRealPath("../../Icons/Arrow/下箭头.png")),QPixmap(GetRealPath("../../Icons/Arrow/上箭头.png")),size=QSize(24,24))
			# fbi=XJQ_FolderBox("列表",QBoxLayout.LeftToRight)
			# fbi.Set_Icon(QPixmap(GetRealPath("../../Icons/Arrow/右箭头.png")),QPixmap(GetRealPath("../../Icons/Arrow/左箭头.png")),size=QSize(32,32))
			fb.Set_Expand(True)
			vbox.addWidget(fb)
			# lv.Opt_AppendWidget(fb)
			cont=fb.Get_Content()
			cont.setStyleSheet('.QWidget{background:rgba(0,128,128,128)}')
			contBox=QVBoxLayout(cont)
			for val in item[1]:
				contBox.addWidget(QPushButton(val))
		vbox.addStretch(1)
		# lv.show()
		self.__wid=wid

	def Opt_Run(self):
		self.__wid.show()
		super().Opt_Run()
		return self.__wid




