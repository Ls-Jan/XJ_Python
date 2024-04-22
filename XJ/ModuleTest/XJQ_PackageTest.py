
__version__='1.0.0'
__author__='Ls_Jan'

from .XJ_PackageInfo import XJ_PackageInfo
from ..Widgets.XJQ_ListWidget import XJQ_ListWidget
from ..Widgets.XJQ_ListWidgetItem import XJQ_ListWidgetItem
from ..Widgets.XJQ_ComboBox import XJQ_ComboBox

import gc
import os
from PyQt5.QtWidgets import QFrame,QGridLayout
from PyQt5.QtGui import QColor, QPaintEvent, QResizeEvent
from PyQt5.QtCore import Qt

__all__=['XJQ_PackageTest']

class XJQ_WidgetBox(QFrame):
	'''
		单纯的容器
	'''
	def __init__(self):
		super().__init__()
		self.__wid=None
	def Set_CenterWidget(self,wid):
		if(self.__wid):
			self.__wid.hide()
			self.__wid.setParent(None)
		if(wid):
			wid.setParent(self)
			wid.setGeometry(0,0,1,1)
			wid.resize(self.size())
			wid.show()
		self.__wid=wid
	def resizeEvent(self, a0: QResizeEvent) -> None:
		if(self.__wid):
			self.__wid.resize(self.size())

class XJQ_PackageTest(QFrame):

	def __init__(self,**groupsPath:str):
		'''
			读取分组下的包信息
		'''
		super().__init__()
		lw=XJQ_ListWidget()
		cb=XJQ_ComboBox()
		wb=XJQ_WidgetBox()

		cb.setMinimumHeight(100)
		cb.Set_List(groupsPath.keys())
		cb.Set_Wheelable(False)
		cb.indexChanged.connect(self.__CB_GroupChange)
		lw.doubleClicked.connect(self.__CB_TestPackage)
		lw.setMinimumWidth(300)

		grid=QGridLayout(self)
		grid.setColumnStretch(0,1)
		grid.setColumnStretch(1,3)
		grid.addWidget(cb,0,0)
		grid.addWidget(lw,1,0)
		grid.addWidget(wb,1,1)
		grid.setAlignment(Qt.AlignCenter)

		groups={}
		for groupName,path in groupsPath.items():
			if(os.path.isdir(path)):
				package=[]
				exclude={'__pycache__'}
				for folder in set(next(os.walk(path))[1]).difference(exclude):
					package.append(XJ_PackageInfo(path,folder))
				groups[groupName]=sorted(package,key=lambda item:-item.Get_MTime(None))#升序排序
		self.__lw=lw
		self.__cb=cb
		self.__groups=groups
		self.__grid=grid
		self.__wb=wb
		self.resize(1400,800)
		self.setStyleSheet('.XJQ_PackageTest{background:#222222}')
		cb.setStyleSheet('color:#AAAAAA;background:#222222')
		wb.setStyleSheet('.XJQ_WidgetBox{background:#444444}')
		# self.setStyleSheet('.XJQ_PackageTest{background:#222222}')
	def __CB_GroupChange(self,index:int,name:str):
		self.__lw.Opt_Clear()
		for package in self.__groups.get(name,[]):
			color={True:QColor(0,128,255),False:QColor(255,255,128)}
			item=XJQ_ListWidgetItem(package.Get_Name(),[package.Get_MTime()],color[package.Get_Test(True)])
			self.__lw.Opt_AppendWidget(item)
	def __CB_TestPackage(self):
		package=self.__groups.get(self.__cb.currentText(),[])[self.__lw.currentRow()]
		test=package.Get_Test()
		self.__currTest=test#防析构
		self.__wb.Set_CenterWidget(None)
		if(test):
			wid=test.Opt_Run()
			self.__wb.Set_CenterWidget(wid)
		gc.collect()#手动收垃圾
			
