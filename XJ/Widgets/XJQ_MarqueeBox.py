from PyQt5.QtWidgets import QWidget,QFrame
from PyQt5.QtCore import Qt,QEvent,QTimer,QPoint,QSize,QRect
from PyQt5.QtGui import QPainter

__all__=['XJQ_MarqueeBox']

class XJQ_MarqueeBox(QFrame):#跑马灯容器
	'''
		跑马灯容器，
		不像烂大街代码只对QLabel进行重写，该跑马灯可以承载其他控件
		仅在鼠标悬浮时运作
		移动速率可调、移动方向可调(四向)、鼠标悬浮时间可调
	'''
	__wid=None
	__hoverTimer=None
	__moveTimer=None
	__stepPixel=None
	__keepOrigin=None
	__horizontal=None
	__snapshoot=None
	__dynamicSnap=None
	__isHover=False
	__autoSize=None
	__offset=0
	__blankPercent=0
	def __init__(self,wid,*,#会给wid控件样式表额外追加“背景透明”的样式，以避免动画的不连贯
			delay=100,#鼠标悬浮一小段时间后开始动画(ms)
			interval=20,#动画刷新间隔(ms)
			pixel=1,#动画每帧平移
			blankPercent=0.25,#空白占比
			horizontal=True,#水平滚动
			forward=True,#正向滚动
			keepOrigin=True,#动画结束后控件位置保持不变
			dynamicSnap=False,#控件的动态截取，静态控件不需要设置该值，避免造成性能损耗
			autoSize=True,#大小自适应，当水平滚动时跑马灯高度随控件，竖直滚动时跑马灯宽度随控件
	):
		super().__init__()
		hTimer=QTimer()
		hTimer.setSingleShot(True)
		hTimer.setInterval(delay)
		hTimer.timeout.connect(self.__StartHovering)
		mTimer=QTimer()
		mTimer.setInterval(interval)
		mTimer.timeout.connect(self.__StepMove)
		wid.setParent(self)

		style=wid.styleSheet()
		if(style.find('{')==-1):
			style+=';\n background:transparent; \n';
		else:
			style+=f'\n .{type(wid).__name__}'+'{background:transparent;}'
		wid.setStyleSheet(style)
		self.setStyleSheet('.XJQ_Marquee{background:transparent}')
		self.__wid=wid
		self.__hoverTimer=hTimer
		self.__moveTimer=mTimer
		self.__stepPixel=pixel if forward else -pixel
		self.__keepOrigin=keepOrigin
		self.__horizontal=horizontal
		self.__blankPercent=blankPercent
		self.__dynamicSnap=dynamicSnap
		self.__autoSize=autoSize
		self.setAttribute(Qt.WA_Hover,True)#设置鼠标悬浮事件：https://blog.csdn.net/chinley/article/details/95404282
		self.installEventFilter(self)
		if(self.__autoSize):
			self.__AdjustSize()
	def Get_Widget(self):
		return self.__wid
	def paintEvent(self,event):
		if(self.__autoSize):
			self.__AdjustSize()
		if(self.__isHover):
			ptr=QPainter(self)
			snapshoot=self.__snapshoot if self.__snapshoot else self.__wid.grab()
			for pos in self.__CalcOffsetPos():
				ptr.drawPixmap(QRect(pos,self.__wid.size()),snapshoot)
	def eventFilter(self,obj,event):
		if(event.type()==QEvent.HoverEnter):
			self.__hoverTimer.start()
		elif(event.type()==QEvent.HoverMove):
			self.__hoverTimer.start()
		elif(event.type()==QEvent.HoverLeave):
			self.__hoverTimer.stop()
			self.__StopHovering()
		else:
			return super().eventFilter(obj,event)
		return True
	def __AdjustSize(self):
		if(self.__horizontal):
			self.setFixedHeight(self.__wid.height())
		else:
			self.setFixedWidth(self.__wid.width())
	def __StartHovering(self):
		if(not self.__isHover):
			self.__isHover=True
			if(not self.__dynamicSnap):
				self.__snapshoot=self.__wid.grab()
			self.__wid.hide()
			self.__moveTimer.start()
	def __StopHovering(self):
		if(self.__isHover):
			self.__isHover=False
			self.__snapshoot=None
			self.__wid.show()
			self.__moveTimer.stop()
			self.update()
			if(not self.__keepOrigin):#位置进行更新
				pos=self.__CalcOffsetPos()[0]
				self.__offset=pos.x() if self.__horizontal else pos.y()
				self.__wid.setGeometry(QRect(pos,self.__wid.size()))
			else:
				self.__offset=0
	def __CalcOffsetPos(self):
		#这块代码，很有“算法”的味道(虽然本质上只是简单的取模操作)
		sizeSelf=self.size()
		sizeWid=self.__wid.size()
		if(self.__horizontal):
			length=sizeWid.width()
			mod=sizeSelf.width()
		else:
			length=sizeWid.height()
			mod=sizeSelf.height()
		if(length<mod):#不需要位移绘制
			return (self.__wid.pos(),)

		blank=mod*self.__blankPercent
		posP=self.__offset%(length+blank)#正值，Positive，靠前的位置
		posN=posP-length-blank#负值，Negative，靠后的位置
		rst=None
		if(self.__horizontal):
			rst=[QPoint(posN,0),QPoint(posP,0)]
		else:
			rst=[QPoint(0,posN),QPoint(0,posP)]
		if(posP<(mod+blank)/2):#如果靠前的显示的内容更多，那就简单调换顺序
			rst.reverse()
		return rst
	def __StepMove(self):
		self.__offset-=self.__stepPixel
		self.update()



