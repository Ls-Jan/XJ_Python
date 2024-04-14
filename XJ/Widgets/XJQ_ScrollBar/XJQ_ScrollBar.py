
__version__='1.1.0'
__author__='Ls_Jan'

from ...Functions.GetRealPath import GetRealPath
from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager

from PyQt5.QtCore import Qt,QRect
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtGui import QColor,QPainter,QPixmap

__all__=['XJQ_ScrollBar']

class XJQ_ScrollBar(QScrollBar):
	'''
		滚动条，舍弃了箭头，风格靠向简约现代型
		(要箭头干嘛？现在多少UI设计的滚动条还要箭头？
	'''
	def __init__(self,*args):
		super().__init__(*args)
		self.__colAdd=QColor(0,0,0,80)
		self.__colSub=QColor(0,255,0,128)
		self.__colHandle_N=QColor(80,80,80)
		self.__colHandle_P=QColor(64,64,64)
		self.__colHandle_H=QColor(96,96,96)
		self.__radiusHandle=15
		self.__radiusGroove=15
		#设置WA_OpaquePaintEvent后控件底色不再是黑色：https://blog.csdn.net/eiilpux17/article/details/116502351
		#但我这里不需要，因为哪怕设置了这玩意儿，绘制出来的效果依旧差，索性不用
		# self.setAttribute(Qt.WA_OpaquePaintEvent,False)
		self.__qss=''
		self.setStyleSheet(GetRealPath('./styleSheet.qss'))
	def setStyleSheet(self,qss:str):
		'''
			设置样式，qss可以是文件路径
		'''
		sm=XJQ_StyleSheetManager()
		sm.setStyleSheet(qss)
		self.__qss=sm.styleSheet()
		self.Opt_UpdateStyleSheet()
	def Set_Radius(self,handle:int=None,groove:int=None):
		'''
			设置滑块和滚动条的倒角半径
		'''
		if(handle!=None):
			self.__radiusHandle=handle
			self.Opt_UpdateStyleSheet()
		if(groove!=None):
			self.__radiusGroove=groove
			self.update()
	def Set_Color(self,
			   add:QColor=None,
			   sub:QColor=None,
			   handleN:QColor=None,
			   handleH:QColor=None,
			   handleP:QColor=None):
		'''
			设置颜色，add、sub为槽的颜色
			handleN、handleH、handleP为滑块的颜色，分别对应于默认、悬浮和拖拽
		'''
		if(add!=None):
			self.__colAdd=add
		if(sub!=None):
			self.__colSub=sub
		if(handleN!=None):
			self.__colHandle_N=handleN
		if(handleH!=None):
			self.__colHandle_H=handleH
		if(handleP!=None):
			self.__colHandle_P=handleP
		self.Opt_UpdateStyleSheet()
	def Opt_UpdateStyleSheet(self):
		'''
			更新样式表(一般不需要手动调用)
		'''
		radius=str(self.__radiusHandle)
		qss=self.__qss.replace('--radiusHandle',radius)
		for item in [
				('--colHandle_N',self.__colHandle_N),
				('--colHandle_H',self.__colHandle_H),
				('--colHandle_P',self.__colHandle_P)]:
			key,col=item
			# col=col.name(QColor.HexArgb)#获取ARGB：https://www.jianshu.com/p/f9bb6f7487f1
			col=col.name()#但这里不需要ARGB，滑块不能透明
			qss=qss.replace(key,col)
		super().setStyleSheet(qss)
		self.update()
	def __GetPressPos(self,mousePos):#获取鼠标点击时滑块的对应位置
		min=self.minimum()#最小值
		wid=self.maximum()-min#取值区间长度
		if(self.orientation()==Qt.Vertical):
			rate=mousePos.y()/self.height()#鼠标点击位置对应滑动条的位置(取值0.0~1.0)
		else:
			rate=mousePos.x()/self.width()#鼠标点击位置对应滑动条的位置(取值0.0~1.0)
		pos=min+int(wid*rate)#鼠标点击位置对应的值
		return pos
	def mousePressEvent(self,event):#避免滑块反复横跳而重写该方法，使滑块总能移动到鼠标附近
		super().mousePressEvent(event)
		cur=self.value()#当前值
		pos=self.__GetPressPos(event.pos())
		if(abs(pos-cur)<self.pageStep()):#点击位置在单步范围内时直接设置为对应值，避免反复横跳
			self.setValue(pos)
	def mouseDoubleClickEvent(self,event):#双击快速跳转指定位
		pos=self.__GetPressPos(event.pos())
		self.setValue(pos)
		super().mouseDoubleClickEvent(event)
	def paintEvent(self,event):
		pix=QPixmap(self.size())
		pix.fill(Qt.transparent)
		ptr=QPainter(pix)
		rect1=QRect(0,0,self.width(),self.height())
		rect2=QRect(rect1)
		length=self.maximum()-self.minimum()+self.pageStep()#参考手册：https://doc.qt.io/qt-5/qscrollbar.html#details
		rate=(self.value()-self.minimum()+self.pageStep()/2)/length
		if(self.orientation()==Qt.Vertical):
			if(self.invertedAppearance()):#反向滚动条
				pos=rect2.height()*(1-rate)
				rect2.setTop(pos)
			else:
				pos=rect2.height()*rate
				rect2.setBottom(pos)
		else:
			if(self.invertedAppearance()):#反向滚动条
				pos=rect2.width()*(1-rate)
				rect2.setLeft(pos)
			else:
				pos=rect2.width()*rate
				rect2.setRight(pos)

		ptr.setCompositionMode(QPainter.CompositionMode_Source)#发现了个好东西
		for item in [(self.__colAdd,rect1),(self.__colSub,rect2)]:
			col,rect=item
			ptr.setBrush(col)
			ptr.setPen(col)
			ptr.drawRoundedRect(rect,self.__radiusGroove,self.__radiusGroove)
		ptr.end()
		ptr=QPainter(self)
		ptr.drawPixmap(0,0,pix)
		super().paintEvent(event)

