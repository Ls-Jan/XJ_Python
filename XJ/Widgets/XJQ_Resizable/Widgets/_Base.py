

from ..Float import Float
from PyQt5.QtGui import QPainter,QTransform
from PyQt5.QtCore import QRect

class Base:
	'''
		可缩放控件基类
	'''
	def __init__(self,rate:Float=Float(1.0)):
		self.__scaleRate=rate
	def setScaleRate(self,rate:Float):
		'''
			设置缩放比率(Float)
		'''
		self.__scaleRate=rate
	def scaleRate(self):
		'''
			获取缩放比率(Float)
		'''
		return self.__scaleRate
	def scaleRect(self,rect:QRect):
		'''
			获取缩放后的矩形
		'''
		rate=self.__scaleRate.val
		return QRect(rect.topLeft(),rect.size()/rate)
	def painter(self):
		'''
			获取设置过QTransform的QPainter
		'''
		rate=self.__scaleRate.val
		ptr=QPainter(self)
		trans=QTransform()
		trans.scale(rate,rate)
		ptr.setTransform(trans)
		return ptr

