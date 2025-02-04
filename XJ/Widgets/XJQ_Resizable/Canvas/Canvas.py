
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['Canvas']

import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt,QRect,QPoint,QChildEvent,QEvent
from PyQt5.QtGui import QWheelEvent,QResizeEvent
from typing import Union,Dict#与py的“类型注解”用法有关：https://zhuanlan.zhihu.com/p/419955374
from ..Float import Float
from ..Widgets._Base import Base
from ._Option import _Option
from ._ScaleRate import _ScaleRate
from ....Structs.XJ_MouseStatus import XJ_MouseStatus

class Canvas(QWidget):#画布容器(抛弃了权重这个笨重的玩意儿)
	'''
		画布类，使用非常简单，控件直接setParent即可加入其中，
		控件的geometry作为逻辑位置，加入画布后仅可通过画布的Set_WidgetPos更新控件的逻辑位置。
		滚轮缩放，右键拖拽(均可禁用)，设置缩放中心(可撤走)，设置缩放值。

		虽然可以向画布中添加任意控件，
		但建议使用XJQ_Resizable.Widgets下的控件以便达到更好的缩放效果(例如字体跟随缩放)。

		不建议创建控件的过程中指定父控件，例如QPushButton("Text",cv)这种创建控件的同时指定父控件
	'''
	__scaleRate:_ScaleRate#缩放极限
	__option:_Option#特殊功能
	__mouseStatus:XJ_MouseStatus#XJ_MouseStatus
	__matrix:np.ndarray#转换矩阵(np.array)，逻辑坐标→显示坐标
	__widPos:Dict[QWidget,QRect]#控件对应的位置
	def __init__(self):
		super().__init__()
		self.__option=_Option()
		self.__scaleRate=_ScaleRate()
		self.__matrix=np.array([[1,0,0],[0,1,0],[0,0,1]])
		self.__mouseStatus=XJ_MouseStatus()
		self.__widPos={}
		self.__scaleRate.curr=Float(1)
	def Set_Option(self,scale:bool=None,drag:bool=None):
		'''
			可以启用/禁用滚轮缩放、鼠标拖拽
		'''
		if(scale==None):
			scale=self.__option.scalable
		if(drag==None):
			drag=self.__option.draggable
		self.__option.scalable=scale
		self.__option.draggable=drag
	def Set_ScaleLimit(self,*,min:int=None,max:int=None):
		'''
			设置缩放极限值
		'''
		if(min!=None):
			self.__scaleRate.min=min
		if(max!=None):
			self.__scaleRate.max=max
	def Set_ScaleCenter(self,obj_or_pos:Union[QWidget,QPoint]):
		'''
			设置缩放中心。
			传入None则缩放时以鼠标位置为准
		'''
		self.__option.scaleCenter=obj_or_pos
	def Set_WidgetPos(self,obj:QWidget,rect:QRect):
		'''
			设置控件逻辑位置。
		'''
		if(obj in self.__widPos and isinstance(rect,QRect)):
			self.__widPos[obj]=rect
			self.__Update(obj)
	def Set_Scale(self,rate,pos:QPoint=None,*,increase:bool=False):
		'''
			设置缩放比，pos为缩放中心(QPoint对象)。
			如果increase为真那么以“增量”的形式调整缩放比(一般用不上)。
			pos指定为None则默认使用画布中心
		'''
		if(pos==None):
			center=self.__option.scaleCenter
			if(isinstance(center,QPoint)):
				pos=self.__MapToPoint(center)[0]
			elif(center in self.__widPos):
				pos=center.geometry().center()
			else:
				sz=self.geometry().size()/2
				pos=QPoint(sz.width(),sz.height())
		if(not increase):
			rate/=self.__matrix[0][0]
		self.__matrix=self.__matrix.dot(np.array([#以鼠标位置为中心进行缩放
				[rate,0,0],
				[0,rate,0],
				[pos.x()*(1-rate),pos.y()*(1-rate),1]
			]))
		self.__scaleRate.curr.val=self.__matrix[0][0]
		self.__Update()
	def Opt_MoveCenterTo(self,obj_or_pos:Union[QWidget,QPoint]):
		'''
			移动画布中心，传入的可以是QPoint也可以是控件对象
		'''
		pos=None
		if(isinstance(obj_or_pos,QPoint)):
			pos=obj_or_pos
		elif(obj_or_pos in self.__widPos):
			pos=self.__widPos[obj_or_pos].center()
		if(pos):
			size=self.size()
			center=QPoint(size.width()>>1,size.height()>>1)
			pos=self.__MapToPoint(pos)[0]
			offset=center-pos
			self.__matrix[2]+=[offset.x(),offset.y(),0]
			self.__Update()
	def Opt_MoveCanvas(self,offset:QPoint):
		'''
			移动画布位置，移动量与鼠标拖拽一致
		'''
		self.__matrix[2]+=[offset.x(),offset.y(),0]
		self.__Update()
	def __Update(self,*objs):
		'''
			更新指定控件的Geometry。
			如果objs为空那么将更新所有对象
		'''
		if(not objs):
			objs=self.__widPos.keys()
		for obj in objs:
			obj.setGeometry(self.__MapToRect(self.__widPos[obj])[0])
		self.update()
	def __MapToPoint(self,*point:QPoint,matrix:np.ndarray=None):
		'''
			将逻辑坐标转化为实际坐标。
			matrix为3*3转换矩阵，默认使用self.__matrix。
		'''
		if(not matrix):
			matrix=self.__matrix
		mat=np.array([[p.x(),p.y(),1] for p in point])
		mat=mat.dot(matrix)#/matrix[2][2]
		return [QPoint(*row[:2]) for row in mat]
	def __MapToRect(self,*rect:QRect,matrix:np.ndarray=None):
		'''
			将逻辑矩形转化为实际坐标。
			matrix为3*3转换矩阵，默认使用self.__matrix。
		'''
		if(not matrix):
			matrix=self.__matrix
		return [QRect(*self.__MapToPoint(r.topLeft(),r.bottomRight())) for r in rect]

	def wheelEvent(self,event:QWheelEvent):
		if(self.__option.scalable):
			pos=None if self.__option.scaleCenter else event.pos()#如果锁定拖拽那么以中心进行缩放
			rate=1+event.angleDelta().y()/1000
			if(self.__matrix[0][0]<self.__scaleRate.min and rate<1):#防止过度缩小
				return
			elif(self.__matrix[0][0]>self.__scaleRate.max and rate>1):#防止过度放大
				return
			self.Set_Scale(rate,pos,increase=True)
	def mousePressEvent(self,event):
		if(self.__option.draggable):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
	def mouseMoveEvent(self,event):
		if(self.__option.draggable):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
			if(ms.Get_PressButtonStatus()[0]==Qt.RightButton):#右键拖拽
				offset=ms.Get_MoveDelta(False)
				self.Opt_MoveCanvas(offset)
	def mouseReleaseEvent(self,event):
		if(self.__option.draggable):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
			self.__Update()
	def resizeEvent(self,event:QResizeEvent):
		'''
			在画布调整大小时始终保持中心位置不变
		'''
		szo=event.oldSize()
		szn=event.size()
		if(szo.isValid() and szo.isValid()):
			dx=szn.width()-szo.width()
			dy=szn.height()-szo.height()
			self.Opt_MoveCanvas(QPoint(dx/2,dy/2))
	def event(self,e:QEvent):
		if(isinstance(e,QChildEvent)):
			# 发现遗留的一坨臭shi，
			# 当使用诸如QPushButton(cv)的方式创建控件时，会向父控件cv发送两发QChildEvent，
			# 第一发是无效的QWidget，第二发才是QPushButton，
			# 并且第一发是QEvent.ChildAdded，第二发是QEvent.ChildPolished，莫名其妙，徒增工作量
			# 字面理解就是第一发的QWidget是作为占位使用的，因为此时还未完全创建出QPushButton实例
			# 但还是很恶心，因为无法判断第二发的QPushButton到底与哪个控件关联
			obj=e.child()
			super().event(e)
			if(isinstance(obj,QWidget)):
				rect=obj.geometry()
				if(e.removed()):
					obj.setGeometry(self.__widPos.pop(obj))#将位置复原
					if(isinstance(obj,Base)):
						obj.setScaleRate(Float(1))
				else:
					if(e.polished()):
						for invalid in set(self.__widPos)-set(self.children()):#清除异端
							self.__widPos.pop(invalid)
					self.__widPos[obj]=rect
					self.__Update(obj)
					if(isinstance(obj,Base)):
						obj.setScaleRate(self.__scaleRate.curr)
		return super().event(e)



