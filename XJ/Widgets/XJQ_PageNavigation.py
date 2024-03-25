
__version__='1.0.0'
__author__='Ls_Jan'

from .XJQ_ComboBox import *
from .XJQ_PureColorIcon import *
from ..Functions.GetRealPath import *

import os
from typing import Union
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QLabel
from PyQt5.QtCore import Qt,pyqtSignal,QSize
from PyQt5.QtGui import QCursor

__all__=['XJQ_PageNavigation']
#TODO：【半成品】页导航栏
class XJQ_PageNavigation(QWidget):#【半成品】页导航栏
	'''
		页导航栏，半成品，按钮少，说好听点就是“精简”
		因为布局空间不足并且目前也没这需求所以没做多按钮的导航栏

		每页显示数可定、数据总数可定，
		当前页展示数据发生变化时发出信号change(int,int)，分别对应数据的索引值和数据个数
	'''
	changed=pyqtSignal(int,int)#切换当前页，发送信号start,count分别对应数据的索引值和数据个数

	__pCount=None#每页数据个数(XJQ_ComboBox)
	__cPage=None#当前页码(XJQ_ComboBox)
	__aBtns=None#箭头按钮
	__countHint=None#额外补充

	__count=None#数据总数
	__pCountTx=lambda self,count:f'{count}条/页'
	__countHintTx=lambda self,:f'总数{self.__count},{self.__cPage.count()}页'
	__pCountLst_Tx=None#pCount文本列表
	__pCountLst_Val=None#pCount数值列表
	__dIndex=0#当前页首个数据对应的索引值
	def __init__(self,*args,iconLeft:str=GetRealPath('../Icons/Arrow/V左箭头.png'),iconRight:str=GetRealPath('../Icons/Arrow/V右箭头.png')):
		super().__init__(*args)
		self.__count=100
		self.__aBtns={'L':QPushButton(),'R':QPushButton()}
		self.__cPage=XJQ_ComboBox(self)
		self.__pCount=XJQ_ComboBox(self)
		self.__countHint=QLabel()

		for key in 'LR':
			btn=self.__aBtns[key]
			btn.setIconSize(QSize(16,16))
			self.__SetCursor(btn,clickable=False)
		self.Set_ArrowIcon(iconLeft,iconRight)
		self.__pCount.indexChanged.connect(lambda index,text:self.Set_PerCount(self.__pCountLst_Val[index]))
		self.__cPage.indexChanged.connect(lambda index,text:self.Set_CurrPage(index+1))
		self.__cPage.Set_ShowArrow(False)
		self.__aBtns['L'].clicked.connect(self.Opt_BackPage)
		self.__aBtns['R'].clicked.connect(self.Opt_NextPage)
		self.Set_PerCountList([10])
		self.__InitUI()
	def Get_CurrIndexCount(self):
		'''
			获取当前页对应的数据索引和数据量
		'''
		count=self.__pCountLst_Val[self.__pCount.currentIndex()]
		page=self.__cPage.currentIndex()
		return page*count,count
	def Set_ArrowIcon(self,iconL:Union[XJQ_PureColorIcon,str]=None,iconR:Union[XJQ_PureColorIcon,str]=None):
		'''
			设置箭头图标
		'''
		if(iconL):
			if(isinstance(iconL,str)):
				iconL=XJQ_PureColorIcon(iconL)
			self.__aBtns['L'].setIcon(iconL)
		if(iconR):
			if(isinstance(iconR,str)):
				iconR=XJQ_PureColorIcon(iconR)
			self.__aBtns['R'].setIcon(iconR)
	def Set_DataCount(self,count:int):
		'''
			设置数据总数
		'''
		self.__count=count
		cPage=self.__cPage
		if True:
			cPage.blockSignals(True)
			pages=count//self.__pCountLst_Val[self.__pCount.currentIndex()]
			if(pages*count<self.__count):
				pages+=1
			self.__cPage.Set_List(range(1,pages+1))
			self.Set_CurrPage(index=self.__dIndex)
			cPage.blockSignals(False)
			self.__countHint.setText(self.__countHintTx())
		return True
	def Set_PerCountList(self,countLst:list):
		'''
			设置每页可选的数据个数
		'''
		lst=[self.__pCountTx(tx) for tx in countLst]
		self.__pCountLst_Tx=lst
		self.__pCountLst_Val=list(countLst)
		self.__pCount.Set_List(lst)
		return True
	def Set_PerCount(self,count:int):
		'''
			设置每页的数据个数
		'''
		pCount=self.__pCount
		cPage=self.__cPage
		if(count in self.__pCountLst_Val):
			pCount.blockSignals(True)
			cPage.blockSignals(True)
			pages=self.__count//count
			if(pages*count<self.__count):
				pages+=1
			self.__cPage.Set_List(range(1,pages+1))
			pCount.setCurrentIndex(self.__pCountLst_Val.index(count))
			self.Set_CurrPage(index=self.__dIndex)
			cPage.blockSignals(False)
			pCount.blockSignals(False)
			self.__countHint.setText(self.__countHintTx())
			return True
		return False
	def Set_CurrPage(self,page:int=0,index:int=0):
		'''
			设置当前页。如果指定index那么将跳转到对应数据所在页
		'''
		cPage=self.__cPage
		count=self.__pCountLst_Val[self.__pCount.currentIndex()]
		if(index>0):
			pageIndex=index//count
		else:
			pageIndex=page-1
		maxPageIndex=cPage.count()-1
		if(pageIndex>maxPageIndex):
			pageIndex=maxPageIndex
		elif(pageIndex<0):
			pageIndex=0
		cPage.blockSignals(True)
		cPage.setCurrentIndex(pageIndex)
		cPage.blockSignals(False)
		self.__SetCursor(self.__aBtns['L'],pageIndex>0)#左箭头
		self.__SetCursor(self.__aBtns['R'],pageIndex<maxPageIndex)#右箭头

		index=pageIndex*count
		count=min(self.__count-index,count)
		if(count<0):
			count=0
		self.__dIndex=index
		self.changed.emit(index,count)
	def Opt_NextPage(self):
		'''
			下一页
		'''
		page=self.__cPage.currentIndex()+1
		if(page<self.__cPage.count()):
			self.Set_CurrPage(page+1)
			return True
		return False
	def Opt_BackPage(self):
		'''
			上一页
		'''
		page=self.__cPage.currentIndex()+1
		if(page>1):
			self.Set_CurrPage(page-1)
			return True
		return False
	
	def __InitUI(self):
		groupL=QWidget()
		groupR=QWidget()
		vboxGL=QVBoxLayout(groupL)
		hboxGR=QHBoxLayout(groupR)
		vboxL=QVBoxLayout()
		vboxR=QVBoxLayout()
		hbox=QHBoxLayout(self)
		vboxGL.addWidget(self.__pCount)
		vboxGL.addWidget(self.__countHint)
		hboxGR.addWidget(self.__aBtns['L'])
		hboxGR.addWidget(self.__cPage)
		hboxGR.addWidget(self.__aBtns['R'])
		vboxL.addStretch(1)
		vboxL.addWidget(groupL)
		# vboxL.addLayout(vboxGL)
		vboxL.addStretch(1)
		vboxR.addStretch(1)
		vboxR.addWidget(groupR)
		# vboxR.addLayout(hboxGR)
		vboxR.addStretch(1)
		hbox.addStretch(1)
		hbox.addLayout(vboxL)
		hbox.addStretch(10)
		hbox.addLayout(vboxR)
		hbox.addStretch(1)
		hbox.setContentsMargins(0,0,0,0)

		self.__cPage.setStyleSheet('''
			QComboBox{
				font-size:20px;
				width:10px;
				background:rgba(0,0,0,0);
			}

			QComboBox QAbstractItemView {
				font-size:20px;
				background-color: rgb(24,24,24);
			}
			QComboBox QAbstractItemView::item {
				height: 30px;
			}

			QComboBox QScrollBar
			{
				background: rgba(255,255,255,5%);
				width: 5px;
			}
			QComboBox QScrollBar::add-line {
				width:0;
				height:0;
			}
			QComboBox QScrollBar::sub-line {
				width:0;
				height:0;
			}
			QComboBox QScrollBar::handle {
				background: rgba(64,64,64,75%);
			}
			QComboBox QScrollBar::sub-page {
				background: rgba(0,0,0,30%);
			}
			QComboBox QScrollBar::add-page {
				background: rgba(0,0,0,30%);
			}
		''')
		self.__pCount.setStyleSheet('''
			QComboBox{
				font-size:17px;
				height:25px;
				background:rgba(0,0,0,30%);
			}
			QComboBox QAbstractItemView {
				font-size:15px;
				background-color: rgb(24,24,24);
			}
			QComboBox QAbstractItemView::item {
				height: 30px;
			}
		''')
		self.__aBtns['L'].setStyleSheet('''
			background:rgba(0,0,0,0);
		''')
		self.__aBtns['R'].setStyleSheet('''
			background:rgba(0,0,0,0);
		''')
		self.__countHint.setText(self.__countHintTx())
		groupR.setStyleSheet('''
			.QWidget{
				background:rgba(0,0,0,20%);
				border-radius:20px;
			}
		''')
	def __SetCursor(self,wid,clickable=True,default=False):
		if(default):
			cursor=Qt.ArrowCursor
		elif(clickable):
			cursor=Qt.PointingHandCursor
		else:
			cursor=Qt.ForbiddenCursor
		wid.setCursor(QCursor(cursor))
