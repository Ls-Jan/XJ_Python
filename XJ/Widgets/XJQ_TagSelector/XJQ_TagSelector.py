
__version__='1.1.0'
__author__='Ls_Jan'


from ..XJQ_Tag import XJQ_Tag
from ..XJQ_SearchBox import XJQ_SearchBox
from ..XJQ_FlowLayout import XJQ_FlowLayout
from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager
from ...Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QVBoxLayout,QFrame,QScrollArea
from PyQt5.QtCore import pyqtSignal

__all__=['XJQ_TagSelector']
class XJQ_TagSelector(QFrame):
	'''
		标签选择器，标签数量过多时搜索会出现卡顿
	'''
	selected=pyqtSignal(str,bool)
	def __init__(self,searchBox:XJQ_SearchBox=None):
		super().__init__()
		sb=XJQ_SearchBox() if searchBox==None else searchBox
		box=QFrame()

		sa=QScrollArea()
		sa.setWidget(box)
		sa.setWidgetResizable(True)
		sb.updated.connect(self.__UpdateSearchBox)
		vbox=QVBoxLayout(self)
		vbox.addWidget(sb)
		vbox.addWidget(sa)
		fbox=XJQ_FlowLayout(box)
		fbox.setContentsMargins(8,8,8,8)

		self.__sa=sa
		self.__sb=sb
		self.__fbox=fbox
		self.__tags={}
		self.setStyleSheet(GetRealPath('./styleSheet.qss'),None)
	def setStyleSheet(self,qss:str,name:str='Main'):
		'''
			name可选值为Main、ScrollBar、ScrollArea、TagsBox、SearchBox。
			qss可为文件路径。
			特别的，如果name直接传None则加载qss中的复数个样式表
		'''
		sm=XJQ_StyleSheetManager()
		sm.setStyleSheet(qss,multi=name==None)
		qss=sm.styleSheet()
		if(name=='Main'):
			super().setStyleSheet(qss)
		elif(name=='ScrollBar'):
			self.__sa.verticalScrollBar().setStyleSheet(qss)
		elif(name=='ScrollArea'):
			self.__sa.setStyleSheet(qss)
		elif(name=='TagsBox'):
			self.__fbox.parent().setStyleSheet(qss)
		elif(name=='SearchBox'):
			self.__sb.setStyleSheet(qss,None)
		elif(name==None):
			for name,qss in sm.styleSheet(returnDict=True).items():
				self.setStyleSheet(qss,name)
	def Get_SearchBox(self):
		'''
			获取搜索框控件
		'''
		return self.__sb
	def Get_TagLst(self,onlySelected:bool=False):
		'''
			获取标签列表，如果onlySelected为真那么将返回被选中的标签
		'''
		lst=[]
		if(onlySelected):
			lst=list(self.__tags)
		else:
			for name,tag in self.__tags.items():
				if(tag.Get_Active()):
					lst.append(name)
		return lst
	def Set_TagStatus(self,tag,isSelected:bool):
		'''
			设置标签的选中状态
		'''
		if(tag in self.__tags):
			tag=self.__tags[tag]
			tag.blockSignals(True)
			tag.Set_Active(isSelected)
			tag.blockSignals(False)
			return True
		return False
	def Set_TagLst(self,tagLst:list):
		'''
			设置标签列表
		'''
		tags=list(self.__tags.values())
		diff=len(tagLst)-len(tags)
		for i in range(diff):
			tag=XJQ_Tag('',clickable=True)
			tag.clicked.connect(self.__ClickTag)
			tags.append(tag)
			self.__fbox.addWidget(tag)
		for i in range(-diff):
			tag=tags.pop()
			self.__fbox.removeWidget(tag)

		self.__tags.clear()
		for i in range(len(tagLst)):
			name=tagLst[i]
			tag=tags[i]
			tag.setText(name)
			tag.Set_Active(False)
			self.__tags[name]=tag
		self.__UpdateSearchBox(self.__sb.text())
	def __UpdateSearchBox(self,tx:str):
		self.__fbox.blockSignals(True)
		for name,tag in self.__tags.items():
			tag.setVisible(tx in name)
		self.__fbox.blockSignals(False)
		self.__fbox.update()
	def __ClickTag(self,flag:bool):
		tag=self.sender()#使用QObject.sender获取信号发送方
		self.selected.emit(tag.text(),tag.Get_Active())
