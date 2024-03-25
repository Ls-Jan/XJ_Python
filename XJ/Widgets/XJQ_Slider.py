
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtCore import Qt,QRect,QPoint,pyqtSignal
from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QColor,QPainter,QPixmap,QMouseEvent

__all__=['XJQ_Slider']

class XJQ_Slider(QSlider):
	'''
		滚动条，滑块是圆圈，风格靠向简约现代型
		同时优化了QSlider的几个使用问题(说难听点就是过时的UI)，使其更贴近用户习惯
		新增“缓存条”样式(参考在线视频播放条)，通过XJQ_Slider.setValue(extra=XX)指定
	'''
	QSS_Base='''
		QSlider{
			background: transparent;
			$dire: $width px
		}
		QSlider::groove{
			background: transparent;
		}
		QSlider::handle{
			width: $width px;
			height: $width px;
			background: qradialgradient(spread:pad, 
				cx:0.5, cy:0.5, radius:0.5, 
				fx:0.5, fy:0.5,
			stop:0.8 $colHandle_N, 
			stop:0.81 transparent);
		}
		QSlider::handle:hover{
			background: qradialgradient(spread:pad, 
				cx:0.5, cy:0.5, radius:0.5, 
				fx:0.5, fy:0.5,
			stop:0.8 $colHandle_H, 
			stop:0.81 transparent);
		}
		QSlider::handle:pressed{
			background: qradialgradient(spread:pad, 
				cx:0.5, cy:0.5, radius:0.5, 
				fx:0.5, fy:0.5,
			stop:0.8 $colHandle_P, 
			stop:0.81 transparent);
		}
	'''
	sliderWheeled=pyqtSignal()#以弥补sliderPress的不足(因为除了鼠标拖拽外还有鼠标滚轮可以修改值，虽然键盘也能修改值，啊麻烦死了)
	def __init__(self,*args):
		super().__init__(*args)
		self.__extraValue=0#新增
		self.__handleWidth=30
		self.__colAdd=QColor(0,0,0,80)
		self.__colSub=QColor(0,255,0,128)
		self.__colExtra=QColor(0,0,255,128)#新增
		self.__colHandle_N=QColor(96,96,96)
		self.__colHandle_P=QColor(64,64,64)
		self.__colHandle_H=QColor(112,112,112)
		self.__radiusGroove=5
		self.__grooveWidth=10
		self.Opt_UpdateStyleSheet()
	def Set_Color(self,
			   add:QColor=None,
			   sub:QColor=None,
			   extra:QColor=None,
			   handleN:QColor=None,
			   handleH:QColor=None,
			   handleP:QColor=None):
		'''
			设置颜色，add、sub、extra为槽的颜色
			handleN、handleH、handleP为滑块的颜色，分别对应于默认、悬浮和拖拽
		'''
		if(add!=None):
			self.__colAdd=add
		if(sub!=None):
			self.__colSub=sub
		if(extra!=None):
			self.__colExtra=extra
		if(handleN!=None):
			self.__colHandle_N=handleN
		if(handleH!=None):
			self.__colHandle_H=handleH
		if(handleP!=None):
			self.__colHandle_P=handleP
		self.Opt_UpdateStyleSheet()
	def setValue(self,value:int=None,extra:int=None):
		'''
			设置当前值，
			特别的，指定extra会有形如“缓存条”的效果
		'''
		if(value!=None):
			super().setValue(value)
		if(extra!=None):
			self.__extraValue=extra
		self.update()
	def Set_HandleWidth(self,width:int):
		'''
			设置滑块大小(直径)
		'''
		self.__handleWidth=width
		lst=[width,0]
		if(self.orientation()==Qt.Horizontal):
			lst.reverse()
		self.setMinimumSize(*lst)
		self.Opt_UpdateStyleSheet()
	def Set_GrooveWidth(self,width:int):
		'''
			设置槽宽
		'''
		self.__grooveWidth=width
		self.update()
	def Opt_UpdateStyleSheet(self):
		'''
			更新样式表(一般不需要手动调用)
		'''
		qss=self.QSS_Base
		for item in [
				('$dire','height' if self.orientation()==Qt.Vertical else 'width'),
				('$width',str(self.__handleWidth)),
				('$colHandle_N',self.__colHandle_N.name()),
				('$colHandle_H',self.__colHandle_H.name()),
				('$colHandle_P',self.__colHandle_P.name())]:
			key,args=item
			qss=qss.replace(key,args)
		self.setStyleSheet(qss)
		self.update()

	def __GetHandlePos(self,mousePos=None,value=None):#获取滑块的对应位置
		if(value==None):
			value=self.value()
		# value=min(self.maximum(),value)
		diff=self.maximum()-self.minimum()
		rate=value/diff if diff>0 else 0
		if(self.invertedAppearance() ^ (self.orientation()==Qt.Vertical)):
			rate=1-rate
		hw=self.__handleWidth
		pos=QPoint(mousePos) if mousePos!=None else QPoint(0,0)
		if(self.orientation()==Qt.Horizontal):
			w=self.width()-hw
			pos.setX(rate*w+hw/2)
		else:
			w=self.height()-hw
			pos.setY(rate*w+hw/2)
		return pos
	def mousePressEvent(self,event):#点击即刻跳转对应位
		# self.setValue(pos)#不用这玩意儿，效果真的太差，采用“拖拽滑块”的方式
		pos=self.__GetHandlePos(event.pos())
		ev=QMouseEvent(event.type(),pos,event.button(),event.buttons(),event.modifiers())
		super().mousePressEvent(ev)#选中滑块
		self.mouseMoveEvent(event)#拖拽滑块
		self.update()
	def mouseMoveEvents(self,event):
		super().mouseMoveEvent(event)
		self.update()
	def wheelEvent(self,event):
		super().wheelEvent(event)
		self.sliderWheeled.emit()
	def paintEvent(self,event):
		pix=QPixmap(self.size())
		pix.fill(Qt.transparent)
		ptr=QPainter(pix)
		rect1=QRect(0,0,self.width(),self.height())
		marginGroove=(self.__handleWidth-min(self.__handleWidth,self.__grooveWidth))/2
		if(self.orientation()==Qt.Vertical):
			rect1.setLeft(rect1.left()+marginGroove)
			rect1.setRight(rect1.right()-marginGroove)
		else:
			rect1.setTop(rect1.top()+marginGroove)
			rect1.setBottom(rect1.bottom()-marginGroove)
		rect2=QRect(rect1)
		rect3=QRect(rect1)
		pos2=self.__GetHandlePos(value=self.__extraValue)
		pos3=self.__GetHandlePos()
		if(self.orientation()==Qt.Vertical):
			pos2=pos2.y()
			pos3=pos3.y()
			if(self.invertedAppearance()):#反向滚动条
				rect2.setTop(pos2)
				rect3.setTop(pos3)
			else:
				rect2.setBottom(pos2)
				rect3.setBottom(pos3)
		else:
			pos2=pos2.x()
			pos3=pos3.x()
			if(self.invertedAppearance()):#反向滚动条
				rect2.setLeft(pos2)
				rect3.setLeft(pos3)
			else:
				rect2.setRight(pos2)
				rect3.setRight(pos3)
		ptr.setCompositionMode(QPainter.CompositionMode_Source)#发现了个好东西
		for item in [(self.__colAdd,rect1),(self.__colExtra,rect2),(self.__colSub,rect3)]:
			col,rect=item
			ptr.setBrush(col)
			ptr.setPen(col)
			ptr.drawRoundedRect(rect,self.__radiusGroove,self.__radiusGroove)
		ptr.end()
		ptr=QPainter(self)
		ptr.drawPixmap(0,0,pix)
		super().paintEvent(event)


