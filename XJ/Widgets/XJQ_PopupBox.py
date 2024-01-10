import math
from PyQt5.QtWidgets import QListView,QWidget,QApplication
from PyQt5.QtCore import Qt,QPoint,QRect,QSize,QRectF
from PyQt5.QtGui import QPainter,QColor,QPainterPath,QPen,QPixmap

__all__=['XJQ_PopupBox']

class XJQ_PopupBox(QWidget):#弹窗式容器，
	'''
		弹窗式容器，其行为可参考组合框点击时弹出的列表，
		只不过可以承载控件而非仅仅的列表，并且点击容器元素时并不会像组合框列表那样消失

		目前的缺点是如果窗口一下缩小到弹窗看不见的大小时弹窗不会更新位置,
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
	#pointAt可以为组件，也可以为QPoint、QRect。当作为后两者时必须额外指定parent
	def __init__(self,pointAt,*,
			parent=None,#指定父控件
			size=None,#指定大小，为None则随容器控件变化
			arrowLength=10,#箭头长度
			arrowWidth=10,#箭头底部宽
			borderThick=4,#边界厚度
			cornerRound=20,#圆角半径
			background=QColor(0,0,0,96),#背景色
			borderColor=QColor(0,0,255),#边界色
			priority='RBLT',#位置优先级，弹窗优先出现的位置
			autoSize=False,):#在无法充分显示时，大小自调节【功能未落实，太靠肝度了】
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
		return self.__content
	def Set_Content(self,wid):
		self.__content.setParent(None)
		self.__content=wid
		wid.setParent(self)
	def Set_Color(self,background=None,border=None):
		if(background):
			self.__bg=background
		if(border):
			self.__bd=border
	def show(self,force=False):
		wid=QApplication.focusWidget()
		if(not force):
			if(wid==self.__trigger):
				self.__trigger=None
				self.hide()
				return
		self.__trigger=wid
		self.setFocus(Qt.MouseFocusReason)
		area=self.__CalcPosition()[2]
		if(area):
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
		pointAt,p,area=self.__CalcPosition()
		if(not pointAt):#不作处理
			self.__cache['pix']=None
			return
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
		pointAt=self.__pointAt
		parent=self.parent()
		if(isinstance(pointAt,QWidget)):
			pointAt=QRect(pointAt.mapTo(parent,QPoint(0,0)),pointAt.size())
		pSize=parent.size()
		if(self.__size):
			cSize=self.__size
		else:
			#参考sizeHint：
			#https://blog.csdn.net/u013087068/article/details/44747621
			#https://blog.csdn.net/qq_40732350/article/details/86703749
			cSize=self.__content.sizeHint()
			if(not cSize):
				cSize=QSize(100,100)
		boxW=cSize.width()+2*self.__thick
		boxH=cSize.height()+2*self.__thick
		lst=[]
		for p in self.__priority:
			L,T,R,B=pointAt.left(),pointAt.top(),pointAt.right(),pointAt.bottom()
			W,H=pSize.width(),pSize.height()
			if(p=='L'):
				area=QRect(QPoint(0,0),QPoint(min(L,W),H))
				line=QRect(pointAt.topLeft(),pointAt.bottomLeft())
			elif(p=='R'):
				area=QRect(QPoint(max(0,R),0),QPoint(W,H))
				line=QRect(pointAt.topRight(),pointAt.bottomRight())
			elif(p=='T'):
				area=QRect(QPoint(0,0),QPoint(W,max(0,T)))
				line=QRect(pointAt.topLeft(),pointAt.topRight())
			elif(p=='B'):
				area=QRect(QPoint(0,min(B,H)),QPoint(W,H))
				line=QRect(pointAt.bottomLeft(),pointAt.bottomRight())
			newline=area.intersected(line)
			if(newline and area):
				W,H=boxW,boxH
				if(p in 'LR'):
					W+=self.__arrowL
				else:
					H+=self.__arrowL
				aW=area.width()
				aH=area.height()
				lst.append((
					newline.center(),
					p,
					area,
					min(aW,W)*min(aH,H)))
				if(aW>W and aH>H):#空间充裕
					if(not area.contains(line)):#边界被截过，作为次要判断
						continue
					else:#理想情况
						lst=lst[-1:]
						break
		if(lst):
			lst.sort(key=lambda item:(-item[3],self.__priority.index(item[1])))
			pointAt,p,area=lst[0][:3]
			x,y=pointAt.x(),pointAt.y()
			W,H=boxW,boxH
			if(p in 'LR'):
				W+=self.__arrowL
				if(p =='L'):
					area.setLeft(area.right()-W+1)
				else:
					area.setRight(area.left()+W-1)
				aT=area.top()+H/2
				aB=area.bottom()-H/2
				if(aT>y):
					aB=aT
				elif(aB<y):
					aT=aB
				else:
					aT=y
					aB=y
				aT-=H/2-1
				aB+=H/2
				area.setTop(aT)
				area.setBottom(aB)
			else:
				H+=self.__arrowL
				if(p =='T'):
					area.setTop(area.bottom()-H+1)
				else:
					area.setBottom(area.top()+H-1)
				aL=area.left()+W/2
				aR=area.right()-W/2
				if(aL>x):
					aR=aL
				elif(aR<x):
					aL=aR
				else:
					aL=x
					aR=x
				aL-=W/2-1
				aR+=W/2
				area.setLeft(aL)
				area.setRight(aR)
			return pointAt,p,area
		return [None,None,None]

