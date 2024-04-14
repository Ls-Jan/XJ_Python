
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_ListWidgetItem import XJQ_ListWidgetItem
from ..XJQ_PureColorIcon import XJQ_PureColorIcon
from ...Functions.GetRealPath import GetRealPath

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout
from PyQt5.QtGui import QColor

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		iconSize_1=(24,24)
		iconSize_2=(32,32)
		icons=[
			XJQ_PureColorIcon(GetRealPath('./已锁.png'),size=iconSize_2,fg=(255,0,0,192)),
			XJQ_PureColorIcon(GetRealPath('./去除.png'),size=iconSize_2,fg=(255,255,0,192)),
			XJQ_PureColorIcon(GetRealPath('./文件袋.png'),size=iconSize_2,fg=(0,255,255,192)),
			XJQ_PureColorIcon(GetRealPath('./收藏.png'),size=iconSize_1,fg=(255,0,255,192)),
			XJQ_PureColorIcon(GetRealPath('./对勾.png'),size=iconSize_1,fg=(0,255,0,192)),]

		wid=QWidget()
		vbox=QVBoxLayout(wid)
		lst=[
			('测试1',['标签1','标签2'],QColor(255,160,0,128),),
			('测试2',['标签1','标签2'],QColor(255,0,0,128),(icons[0],)),
			('测试3',['标签1','标签2','标签3','标签4'],QColor(0,0,255,128),(icons[3],icons[4])),
			('测试4',['标签1','标签2'],QColor(255,160,0,128),(icons[1],)),
			('测试5',['标签1','标签2'],QColor(0,0,255,128),(icons[2],)),
			]
		for data in lst:
			vbox.addWidget(XJQ_ListWidgetItem(*data))
		wid.setStyleSheet('background:#222222')
		self.__wid=wid

	def Opt_Run(self):
		self.__wid.resize(300,400)
		self.__wid.show()
		return super().Opt_Run()





