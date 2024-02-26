


__version__='1.0.0'
__author__='Ls_Jan'
from typing import Union

from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtWidgets import QWidget,QWIDGETSIZE_MAX
from PyQt5.QtGui import QColor,QPainter,QPen

__all__=['XJQ_SepLine']

class XJQ_SepLine(QWidget):
	'''
		分隔线。功能简单粗暴，支持粗细、方向、颜色、线样式(默认实线)
	'''
	def __init__(self,
			orientation:Qt.Orientation=Qt.Horizontal,
			thick:int=1,
			margin:Union[int,tuple]=0,
			color:QColor=QColor(),
			style:Qt.PenStyle=Qt.SolidLine):
		'''
			orientation为分隔方向，默认水平(也就是竖线形式)。
			thick为分隔线粗细。
			color为分隔线颜色。
			margin为分割线两侧的空白。
			style为分隔线样式，默认实线绘制。
		'''
		super().__init__()
		self.__orientation=orientation
		self.__thick=thick
		self.__color=color
		self.__style=style
		self.__margin=margin
		self.Set_Margin(margin)
		self.__Update()
	def Set_Style(self,style:Qt.PenStyle):
		'''
			设置分隔线样式，效果可参考手册：https://doc.qt.io/qt-6/qt.html#PenStyle-enum
			默认实线Qt.SolidLine
		'''
		self.__style=style
		self.update()
	def Set_Color(self,color:QColor):
		'''
			设置颜色
		'''
		self.__color=color
		self.update()
	def Get_Color(self):
		'''
			获取颜色
		'''
		return self.__color
	def Set_Thick(self,thick:int):
		'''
			设置分隔线厚度
		'''
		self.__thick=thick
		self.__Update()
	def Set_Margin(self,margin:Union[int,tuple]):
		'''
			设置分隔线占据的空白
		'''
		if(isinstance(margin,int)):
			margin=(margin,margin)
		self.__margin=margin
		self.__Update()
	def Set_Orientation(self,orientation:Qt.Orientation):
		'''
			设置分隔方向
		'''
		self.__orientation=orientation
		self.__Update()
	def Get_Style(self):
		'''
			获取分隔线样式
		'''
		return self.__style
	def Get_Thick(self):
		'''
			获取分隔线厚度
		'''
		return self.__thick
	def Get_Orientation(self):
		'''
			获取分隔方向
		'''
		return self.__orientation
	def __Update(self):
		'''
			QWidget.setFixedSize本质上就是把最大最小值都设置为固定值。
			https://blog.csdn.net/cOnhthefroad/article/details/109466417
		'''
		t=sum(self.__margin)+self.__thick
		self.setFixedSize(t,t)
		if(self.__orientation==Qt.Horizontal):
			self.setMinimumHeight(1)
			self.setMaximumHeight(QWIDGETSIZE_MAX)
		else:
			self.setMinimumWidth(1)
			self.setMaximumWidth(QWIDGETSIZE_MAX)
		self.update()
	def paintEvent(self,event):
		ptr=QPainter(self)
		pen=QPen()
		pen.setStyle(self.__style)
		pen.setColor(self.__color)
		pen.setWidth(self.__thick)
		ptr.setPen(pen)
		p1=QPoint(0,0)
		p2=QPoint(self.width(),self.height())
		w,h=self.__margin
		if(self.__orientation==Qt.Horizontal):
			p1.setX(w)
			p2.setX(w)
		else:
			p1.setY(w)
			p2.setY(w)
		ptr.drawLine(p1,p2)
