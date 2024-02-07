
__version__='1.0.0'
__author__='Ls_Jan'

from .XJQ_MouseStatus import *

import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt,QRect,QPoint,QChildEvent,QTimer
from PyQt5.QtGui import QPainter,QMouseEvent

__all__=['XJQ_CanvasBox']
class XJQ_CanvasBox(QWidget):#画布容器(抛弃了权重这个笨重的玩意儿)
	'''
		画布类，使用非常简单，
		控件直接setParent即可加入其中(控件的geometry作为逻辑位置)
		加入画布后的控件调用setGeometry之类的函数不会有实际意义，
		可通过画布的Set_WidgetPos来更新控件的逻辑位置

		滚轮缩放，右键拖拽(均可禁用)，设置缩放中心(可撤走)，设置缩放值，
		画布控件缩放时会进行简单的同步缩放(可禁用)
	'''
	__scaleLimit={#缩放极限
		'min':0.5,
		'max':10}
	__option={#功能
		'scale':True,
		'drag':True,
		'autoScale':True,
		'center':None}#逻辑位置，QPoint/QWidget对象
	__range=QRect()#控件的总范围(逻辑位置)
	__poses={}#{obj:QRect}#控件对应逻辑位置
	__matrix=None#转换矩阵(np.array)，逻辑坐标→显示坐标
	__mouseStatus=None#XJQ_MouseStatus
	__snapshoot={#用于解决画布拖拽及缩放时的卡顿问题
		'img':None,#QPixmap
		'rect':None,}#QRect
	__timer=None#定时器，滚轮缩放时定时刷新画面
	def __init__(self):
		super().__init__()
		self.__poses={}
		self.__option=self.__option.copy()
		self.__matrix=np.array([[3,0,0],[0,3,0],[0,0,1]])
		self.__mouseStatus=XJQ_MouseStatus()
		self.__timer=QTimer()
		self.__timer.setSingleShot(True)
		self.__timer.timeout.connect(self.__WheelDelay)
		self.installEventFilter(self)
		self.Set_WheelDelay()
	def Set_Option(self,scale=None,drag=None,autoScale=None):#设置功能
		if(scale==None):
			scale=self.__option['scale']
		if(drag==None):
			drag=self.__option['drag']
		if(autoScale==None):
			autoScale=self.__option['autoScale']
		self.__option['drag']=drag
		self.__option['scale']=scale
		self.__option['autoScale']=autoScale
	def Set_WheelDelay(self,delay=100):#滚轮缩放时刷新画面的时间间隔(默认100ms)
		self.__timer.setInterval(delay)
	def Set_ScaleLimit(self,*,min=0,max=0):#设置缩放极限值
		if(min!=0):
			self.__scaleLimit['min']=min
		if(max!=0):
			self.__scaleLimit['max']=max
	def Opt_MoveCenter(self,obj_or_pos,lock=False):#移动画布中心，传入的可以是QPoint也可以是控件对象
		pos=None
		if(isinstance(obj_or_pos,QPoint)):
			pos=obj_or_pos
		elif(obj_or_pos in self.__poses):
			pos=self.__poses[obj_or_pos].center()
		if(pos):
			size=self.size()
			center=QPoint(size.width()>>1,size.height()>>1)
			pos=self.__MapToRealPoint(pos)[0]
			offset=center-pos
			self.__matrix[2]+=[offset.x(),offset.y(),0]
			self.__Update()
			if(lock):
				self.__option['center']=obj_or_pos
	def Set_WidgetPos(self,obj,pos):#设置控件逻辑位置
		if(obj in self.__poses and isinstance(pos,QRect)):
			self.__poses[obj]=pos
		rect=QRect()
		for obj in self.__poses:
			rect=rect.united(obj.geometry())
		self.__range=rect
	def Set_Scale(self,rate,pos=None,increase=False):#设置缩放，pos为缩放中心(QPoint对象)
		if(pos==None):
			center=self.__option['center']
			if(isinstance(center,QPoint)):
				pos=self.__MapToRealPoint(center)[0]
			elif(center in self.__poses):
				pos=center.geometry().center()
			else:
				sz=self.geometry().size()/2
				pos=QPoint(sz.width(),sz.height())
		if(not increase):
			rate/=self.__matrix[0][0]
		self.__matrix=self.__matrix.dot(np.array([[rate,0,0],[0,rate,0],[pos.x()*(1-rate),pos.y()*(1-rate),1]]))#以鼠标位置为中心进行缩放
		self.__Update()
	def __Update(self,*objs):#更新指定控件的Geometry。如果objs为空那么将更新所有对象
		if(not objs or not objs[0]):
			objs=self.__poses.keys()
		for obj in objs:
			obj.setGeometry(*self.__MapToRealRect(self.__poses[obj]))
		self.update()
	def __HideWidgets(self,exclude=set()):#将除了exclude以外的控件全部隐藏
		for obj in self.__poses:
			if(obj not in exclude):
				obj.hide()
	def __ShowWidgets(self):#显示所有控件
		for obj in self.__poses:
			obj.show()
	def __GetIMatrix(self):#获取逆矩阵
		return np.linalg.inv(self.__matrix)
	def __GrapSnapShoot(self):#抓取快照
		size=self.size()
		rect_1=self.__range
		rect_2=QRect(QPoint(-size.width(),-size.height()),3*size)
		rect_2=self.__MapToRect(self.__GetIMatrix(),rect_2)[0]#求逻辑位置
		rect=rect_1.intersected(rect_2)#取交集
		return {'rect':rect,'img':self.grab(self.__MapToRealRect(rect)[0])}
	def __MapToRealPoint(self,*logicPoint):
		return self.__MapToPoint(self.__matrix,*logicPoint)
	def __MapToRealRect(self,*logicRect):
		return self.__MapToRect(self.__matrix,*logicRect)
	def __MapToPoint(self,matrix,*point):
		mat=np.array([[p.x(),p.y(),1] for p in point])
		mat=mat.dot(matrix)#/matrix[2][2]
		return [QPoint(*row[:2]) for row in mat]
	def __MapToRect(self,matrix,*rect):
		return[QRect(*self.__MapToPoint(matrix,r.topLeft(),r.bottomRight())) for r in rect]
	def __WheelDelay(self):#用于wheelEvent的延迟动作
		self.__snapshoot['img']=None
		self.__Update()
		self.__ShowWidgets()

	def eventFilter(self,obj,e):
		if(isinstance(e,QChildEvent)):
			obj=e.child()
			rect=obj.geometry()
			if(e.added()):
				self.__poses[obj]=rect
				self.__Update(obj)
				self.Set_WidgetPos(obj,rect)
			elif(e.removed()):
				rect=self.__poses.pop(obj)
				obj.setGeometry(rect)#将位置复原
				self.Set_WidgetPos(None,None)
		return super().eventFilter(obj,e)
	def wheelEvent(self,event):
		if(self.__option['scale']):
			if(not self.__timer.isActive()):
				self.__snapshoot=self.__GrapSnapShoot()
				self.__HideWidgets()#隐藏组件
				self.__timer.start()
			pos=None if self.__option['drag'] else event.pos()#如果锁定拖拽那么以中心进行缩放
			rate=1+event.angleDelta().y()/1000
			if(self.__matrix[0][0]<self.__scaleLimit['min'] and rate<1):#防止过度缩小
				return
			elif(self.__matrix[0][0]>self.__scaleLimit['max'] and rate>1):#防止过度放大
				return
			self.Set_Scale(rate,pos,increase=True)
	def mousePressEvent(self,event):
		if(self.__option['drag']):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
			self.__snapshoot=self.__GrapSnapShoot()
			self.__HideWidgets({wid for wid in self.__poses if wid.underMouse()})
	def mouseMoveEvent(self,event):
		if(self.__option['drag']):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
			if(ms.Get_PressButtonStatus()[0]==Qt.RightButton):#右键拖拽
				offset=ms.Get_MoveDelta(False)
				self.__matrix[2]+=[offset.x(),offset.y(),0]
				self.__Update()
	def mouseReleaseEvent(self,event):
		if(self.__option['drag']):
			ms=self.__mouseStatus
			ms.Opt_Update(event)#更新鼠标状态
			self.__snapshoot['img']=None
			self.__ShowWidgets()
			self.__Update()
	def paintEvent(self,event):
		if(self.__snapshoot['img']):#该值在鼠标按下或者滚轮滚动时赋值，鼠标抬起时将被清除
			ptr=QPainter(self)
			rect=self.__MapToRealRect(self.__snapshoot['rect'])[0]
			ptr.drawPixmap(rect,self.__snapshoot['img'])
		else:
			super().paintEvent(event)
	def resizeEvent(self,event):
		if(self.__option['autoScale']):
			szo=event.oldSize()
			szn=event.size()
			if(szo.isValid() and szo.isValid()):
				rX=szn.width()/szo.width()
				rY=szn.height()/szo.height()
				rate=min(rX,rY) if rX<1 or rY<1 else max(rX,rY)
				self.Set_Scale(rate,increase=True)
				self.Opt_MoveCenter(self.__option['center'])


