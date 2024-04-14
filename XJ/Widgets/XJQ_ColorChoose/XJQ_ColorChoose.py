
__version__='1.0.0'
__author__='Ls_Jan'

from typing import Union#与py的“类型注解”用法有关：https://zhuanlan.zhihu.com/p/419955374
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel,QColorDialog,QWidget


__all__=['XJQ_ColorChoose']

class XJQ_ColorChoose(QLabel):#小控件，点击弹出换色窗口
	'''
		不继承QPushButton，这玩意儿总能给我开眼，
		调用QPushButton.setFlat(True)后样式表设置的背景色失效，我愣是查半小时原因才发现是这**
	'''
	valueChanged=pyqtSignal(tuple)#槽信号，值修改时发送信号
	def __init__(self,parent:QWidget=None,color:Union[QColor,tuple]=(255,50,50,255),hasAlpha:bool=True):
		'''
			color可为元组或者QColor对象
			hasAlpha为真则带有透明度
		'''
		super().__init__(parent)
		self.setCursor(Qt.PointingHandCursor)
		self.setMinimumSize(32,32)
		self.__color=QColor()
		self.__hasAlpha=hasAlpha
		self.Set_Color(color)
	def Set_Color(self,color:Union[QColor,tuple]):
		'''
			color可为元组或者QColor对象
		'''
		if(not isinstance(color,QColor)):
			if(not self.__hasAlpha):
				color=color[:3]
			color=QColor(*color)
		self.__color=color
		self.__SetColor()
		self.valueChanged.emit(self.Get_Color())#值修改时发送信号
	def Get_Color(self,isTuple=True):
		'''
			返回rgba，isTuple为真则返回元组，否则返回QColor
		'''
		col=self.__color
		return (col.red(),col.green(),col.blue(),col.alpha()) if isTuple else col
	def __SetColor(self):
		self.setStyleSheet("background:rgba{0}".format(self.Get_Color()))#设置颜色
		self.update()
	def mousePressEvent(self,event):#设置点击事件
		if event.button()==Qt.LeftButton:#左键点击
			#支持alpha通道：https://blog.csdn.net/can3981132/article/details/52241586
			if(self.__hasAlpha):
				col=QColorDialog.getColor(self.__color,options=QColorDialog.ShowAlphaChannel)
			else:
				col=QColorDialog.getColor(self.__color)
			if(col.isValid()):
				self.__color=col
				self.__SetColor()
				self.valueChanged.emit(self.Get_Color())#值修改时发送信号

