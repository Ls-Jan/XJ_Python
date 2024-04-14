
__version__='1.0.0'
__author__='Ls_Jan'

from ...Functions.CalcPopupArea import *

import math
from typing import Union
from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtCore import Qt,QPoint,QRect,QSize,QRectF
from PyQt5.QtGui import QPainter,QColor,QPainterPath,QPen,QPixmap

__all__=['XJQ_PopupBox']

class XJQ_PopupBox(QWidget):#弹窗式容器，
	'''
		弹窗式容器，其行为可参考组合框点击时弹出的列表，
		只不过可以承载控件而非仅仅的列表，并且点击容器元素时并不会像组合框列表那样消失

		目前的缺点是如果窗口一下缩小到弹窗看不见的大小时弹窗不会更新位置(这个漏洞得大动刀才能修，说实话不想搞),
		只不过这个问题影响不大，连调用两次show()即可
	'''
	__size=None
	__content=None
	__arrowL=None
	__arrowW=None
	__priority=None
	__autoSize=None#大小自调节【功能未落实，太靠肝度了】
	__pointAt=None
	__trigger=None
	__bg=None
	__bd=None
	__round=None
	__thick=None
	__cache={'pSize':None,'cRect':None,'pix':None}#绘制缓存
	def __init__(self,pointAt:Union[QWidget,QPoint,QRect],*,#pointAt可以为组件，也可以为QPoint、QRect。当作为后两者时必须额外指定parent
			parent:QWidget=None,#指定父控件
			size:QSize=None,#指定大小，为None则随容器控件变化
			arrowLength:int=10,#箭头长度
			arrowWidth:int=10,#箭头底部宽
			borderThick:int=4,#边界厚度
			cornerRound:int=20,#圆角半径
			background:QColor=QColor(0,0,0,96),#背景色
			borderColor:QColor=QColor(0,0,255),#边界色
			priority:str='RBLT',#位置优先级，弹窗优先出现的位置
			autoSize:bool=False,):#在无法充分显示时，大小自调节【功能未落实，太靠肝度了】
		'''
			pointAt：可以为组件，也可以为QPoint、QRect。当作为后两者时必须额外指定parent
			parent：指定父控件，不显式指定的话会自动寻找pointAt的顶级父控件
			size：指定大小，为None则随容器控件变化
			arrowLength：箭头长度
			arrowWidth：箭头底部宽
			borderThick：边界厚度
			cornerRound：圆角半径
			background：背景色
			borderColor：边界色
			priority：位置优先级，弹窗优先出现的位置
			autoSize：在无法充分显示时，大小自调节【功能未落实，太靠肝度了】
		'''
		super().__init__()
		if(isinstance(pointAt,QWidget)):
			temp=pointAt
			while(True):
				if(temp==parent):
					break
				if(temp.parent()==None):
					parent=temp
					break
				temp=temp.parent()
		elif(isinstance(pointAt,QPoint)):
			pointAt=QRect(pointAt,pointAt)
		elif(isinstance(pointAt,QRect)):
			pass
		else:
			raise Exception('类型错误！XJQ_PopupBox对象初始化参数pointAt异常')
		if(parent==None):
			raise Exception('参数不足！XJQ_PopupBox对象初始化参数parent缺失')

		content=QWidget(self)
		self.__size=None
		self.__content=content
		self.__arrowL=arrowLength
		self.__arrowW=arrowWidth
		self.__autoSize=autoSize
		self.__pointAt=pointAt
		self.__priority=priority.upper() if priority else 'RBLT'
		self.__cache=self.__cache.copy()
		self.__thick=borderThick
		self.__round=cornerRound
		self.__bg=background
		self.__bd=borderColor
		self.resize(size)
		self.setParent(parent)
		self.setStyleSheet('.XJQ_PopupBox{background:transparent;}')#避免无意间被染色，毕竟样式表的背景绘制无法被paintEvent拦截
	def Get_Content(self):
		'''
			获取内容物
		'''
		return self.__content
	def Set_Content(self,wid:QWidget):
		'''
			设置内容物
		'''
		self.__content.setParent(None)
		self.__content=wid
		wid.setParent(self)
	def Set_Color(self,background:QColor=None,border:QColor=None):
		'''
			设置背景色以及边界色
		'''
		if(background):
			self.__bg=background
		if(border):
			self.__bd=border

	def show(self,force=False):
		'''
			force为假时会根据当前聚焦控件来判断是否进行显示
		'''
		wid=QApplication.focusWidget()
		if(not force):
			if(wid==self.__trigger):
				self.__trigger=None
				self.hide()
				return
		self.__trigger=wid
		self.setFocus(Qt.MouseFocusReason)
		rst=self.__CalcPosition()
		if(rst):
			area=rst[2]
			self.setGeometry(area)
			super().show()
	def resize(self,size):
		self.__size=size
	def paintEvent(self,event):
		wid=QApplication.focusWidget()
		if(wid!=self.focusWidget()):
			self.hide()
			if(wid!=self.__trigger):
				self.__trigger=None

		self.__UpdateCache()
		pix=self.__cache['pix']
		if(not pix):#容器控件在区域外，隐藏不显示
			self.__trigger=None
			self.hide()
			return
		ptr=QPainter(self)
		ptr.drawPixmap(0,0,pix)
	def __UpdateCache(self):#更新缓存__cache，同时设置geometry属性。(只是将原本堆在paintEvent的大量代码转移过来罢了
		if(self.__cache['pSize']==self.parent().size() and self.__cache['cRect']==self.__content.geometry()):
			return
		rst=self.__CalcPosition()
		if(not rst):
			self.__cache['pix']=None
			return
		pointAt,p,area=rst

		self.setGeometry(area)
		x,y=pointAt.x(),pointAt.y()
		aW=self.__arrowW
		aL=self.__arrowL
		r=self.__round
		t=self.__thick
		T,B,L,R=area.top(),area.bottom(),area.left(),area.right()
		lst=[]
		if(p in 'LR'):
			a=T+r+aW/2
			b=B-r-aW/2
			if(a>y):
				b=a
			elif(b<y):
				a=b
			else:
				a=y
				b=y
			a-=aW/2
			b+=aW/2
			if(p=='L'):
				R-=aL
				lst.append(QPoint(R-t/2,b))
				lst.append(pointAt)
				lst.append(QPoint(R-t/2,a))
			else:
				L+=aL
				lst.append(QPoint(L+t/2,a))
				lst.append(pointAt)
				lst.append(QPoint(L+t/2,b))
		else:
			a=L+r+aW/2
			b=R-r-aW/2
			if(a>x):
				b=a
			elif(b<x):
				a=b
			else:
				a=x
				b=x
			a-=aW/2
			b+=aW/2
			if(p=='T'):
				B-=aL
				lst.append(QPoint(a,B-t/2))
				lst.append(pointAt)
				lst.append(QPoint(b,B-t/2))
			else:
				T+=aL
				lst.append(QPoint(b,T+t/2))
				lst.append(pointAt)
				lst.append(QPoint(a,T+t/2))
		TK=QPoint(t/2,t/2)
		LT=self.mapFrom(self.parent(),QPoint(L,T))
		RB=self.mapFrom(self.parent(),QPoint(R,B))
		lst=[self.mapFrom(self.parent(),p) for p in lst]
		LT+=TK
		RB-=TK

		path=QPainterPath()#path以逆时针装载
		path.moveTo(lst[0])
		for point in lst[1:]:
			path.lineTo(point)
		LT+=QPoint(1,1)#经常出现差1像素的问题，见怪不怪。
		angle='LBRT'.index(p)*90
		rect=QRect(LT,RB)
		rw=rect.width()/2
		rh=rect.height()/2
		rx=rect.center().x()
		ry=rect.center().y()
		startPoint=QPoint(rx+math.cos(math.radians(angle))*rw,ry-math.sin(math.radians(angle))*rh)
		for i in range(4):#逆时针
			rangle=math.radians(angle+45)
			sinR=-math.sin(rangle)
			cosR=math.cos(rangle)
			x=rx+math.copysign(rw,cosR)
			y=ry+math.copysign(rh,sinR)
			cx=rx+math.copysign(1,cosR)*(rw-self.__round)
			cy=ry+math.copysign(1,sinR)*(rh-self.__round)
			path.arcTo(QRectF(QPoint(x,y),QPoint(cx,cy)).normalized(),angle,90)
			angle+=90
		path.lineTo(lst[0])#形成封闭图形

		pix=QPixmap(self.size())
		pix.fill(Qt.transparent)
		ptr=QPainter(pix)
		ptr.setBrush(self.__bg)
		ptr.setPen(QPen(self.__bd,self.__thick))
		ptr.drawPath(path)
		ptr.end()

		LT+=TK
		RB-=TK
		LT-=QPoint(2,2)#再找就太麻烦了，已经调了一个多小时就为了那么几像素偏差
		RB-=QPoint(1,1)
		self.__content.setGeometry(QRect(LT,RB))
		self.__cache['pSize']=self.parent().size()
		self.__cache['cRect']=self.__content.geometry()
		self.__cache['pix']=pix
	def __CalcPosition(self):#计算位置，将依次返回：目标坐标(QPoint)、弹窗所在方位(LTRB之一)、弹窗所在区域(QRect)
		target=self.__pointAt
		parent=self.parent()
		if(isinstance(target,QWidget)):
			target=QRect(target.mapTo(parent,QPoint(0,0)),target.size())
		pSize=parent.size()
		if(self.__size):
			hSize=self.__size
		else:
			#参考sizeHint：
			#https://blog.csdn.net/u013087068/article/details/44747621
			#https://blog.csdn.net/qq_40732350/article/details/86703749
			hSize=self.__content.sizeHint()
			if(not hSize):
				hSize=QSize(100,100)
		return CalcPopupArea(target,hSize,pSize,self.__arrowL,priority=self.__priority)
