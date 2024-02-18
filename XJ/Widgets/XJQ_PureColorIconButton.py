

__version__='1.0.0'
__author__='Ls_Jan'

from .XJQ_PureColorIcon import *

from PyQt5.QtCore import QSize,QRect,QPoint,Qt
from PyQt5.QtGui import QIcon,QPixmap,QPainter,QBitmap,QColor,QCursor
from PyQt5.QtWidgets import QAbstractButton

__all__=['XJQ_PureColorIconButton']
class XJQ_PureColorIconButton(QAbstractButton):
	'''
		基于XJQ_PureColorIcon的可改色图标按钮(无文本)

		简单试过，QLabel.setPixmap会复制pixmap，真的是，无语，索性直接重写paintEvent。
		原本继承QWidget，但后来想想为了减少风险(同时也让代码更加规范)还是选择继承QAbstractButton
	'''
	def __init__(self,iconData=None,parent=None):
		'''
			iconData将直接传给XJQ_PureColorIcon
		'''
		super().__init__(parent)
		self.__rRadius=20
		self.__rMask=False
		self.__cMask=False
		self.__icon=None
		self.__status='default'
		self.__cache={
			'default':{'fg':QColor(224,224,224,255),'bg':QColor(0,0,0,0),'pix':None},
			'hover':{'fg':QColor(255,255,255,255),'bg':QColor(0,0,0,0),'pix':None},
			'pressed':{'fg':QColor(160,160,160,255),'bg':QColor(0,0,0,0),'pix':None},
			'disable':{'fg':QColor(224,224,224,128),'bg':QColor(0,0,0,0),'pix':None},
		#虽然看似很多，但因为图标都很小，它们对内存的影响可谓忽略不计
		#以64*64*4字节为例，一个pixmap占16kb左右，一组4个，即64KB，
		#即16个XJQ_PureColorIconButton对象的图片占用内存才1MB
		}
		self.setIcon(iconData)
		self.setDisabled(False)
	def setIcon(self,iconData):
		'''
			iconData将直接传给XJQ_PureColorIcon
		'''
		if(self.__icon):
			size=self.__icon.size()
		else:
			size=QSize(32,32)
		self.__icon=XJQ_PureColorIcon(iconData)
		self.__icon.resize(size)
		self.__UpdateCache()
	def Set_FgColor(self,default:QColor=None,hover:QColor=None,pressed:QColor=None,disable:QColor=None):
		'''
			设置前景色
		'''
		keys=[]
		for key in self.__cache:
			val=eval(key)
			if(val):
				self.__cache[key]['fg']=val
				keys.append(key)
		self.__UpdateCache(*keys)
	def Set_BgColor(self,default:QColor=None,hover:QColor=None,pressed:QColor=None,disable:QColor=None):
		keys=[]
		for key in self.__cache:
			val=eval(key)
			if(val):
				self.__cache[key]['bg']=val
				keys.append(key)
		self.__UpdateCache(*keys)

	def resizeEvent(self,event):
		self.resize(event.size())
	def resize(self,*size):
		if(len(size)==2):
			size=QSize(*size)
		else:
			size=size[0]
		self.__icon.resize(size)
		size=self.__icon.size()
		if(True):
			super().resize(size)
			self.__UpdateCache()
			self.Set_Mask(roundRect=self.__rMask,circle=self.__cMask)
	def setGeometry(self,*args):
		rect=QRect(*args)
		self.resize(rect.size())
		super().move(rect.topLeft())
	def setDisabled(self,flag):
		if(flag):
			self.__status='disable'
			self.setCursor(QCursor(Qt.ForbiddenCursor))
		else:
			self.__status='default'
			self.setCursor(QCursor(Qt.PointingHandCursor))
		super().setDisabled(flag)
	def Set_Mask(self,*,roundRect=False,circle=False,roundRectRadius=None):
		if(roundRectRadius!=None and roundRectRadius>0):
			self.__rRadius=roundRectRadius
		self.__rMask=roundRect
		self.__cMask=circle
		bit=QBitmap(self.size())
		bit.fill(Qt.white)
		if(roundRect or circle):
			bptr=QPainter(bit)
			bptr.setBrush(Qt.black)
			rect=QRect(QPoint(0,0),self.size())
			if(roundRect):
				bptr.drawRoundedRect(rect,self.__rRadius,self.__rRadius)
			else:
				bptr.drawEllipse(rect)
			bptr.end()
		self.setMask(bit)
	def paintEvent(self,event):
		ptr=QPainter(self)
		ptr.drawPixmap(0,0,self.__cache[self.__status]['pix'])
	def enterEvent(self,event):
		if(self.__SetStatus('hover')):
			self.update()
	def leaveEvent(self,event):
		if(self.__SetStatus('default')):
			self.update()
	def mouseMoveEvent(self,event):
		pass
	def mousePressEvent(self,event):
		if(self.__SetStatus('pressed')):
			self.update()
	def mouseReleaseEvent(self,event):
		if(self.__SetStatus('hover')):
			#鼠标位置判断：https://blog.csdn.net/uriel_chiang/article/details/79626911
			#虽然才知道有underMouse这个方法，但实用下来发现有问题，不采用
			# if(self.underMouse()):
			if(self.rect().contains(event.pos())):
				self.clicked.emit()
			self.update()
	def __SetStatus(self,stat):
		if(self.__status!='disable'):
			self.__status=stat
			return True
		return False
	def __UpdateCache(self,*keys):
		if(len(keys)==0):
			keys=self.__cache.keys()
		for key in keys:
			item=self.__cache[key]
			self.__icon.Set_Color(item['fg'],item['bg'])
			item['pix']=self.__icon.pixmap()

