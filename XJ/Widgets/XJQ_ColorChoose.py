
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel,QColorDialog


__all__=['XJQ_ColorChoose']

class XJQ_ColorChoose(QLabel):#小控件，点击弹出换色窗口
	'''
		不继承QPushButton，这玩意儿总能给我开眼，
		调用QPushButton.setFlat(True)后样式表设置的背景色失效，我愣是查半小时原因才发现是这**
	'''
	valueChanged=pyqtSignal(tuple)#槽信号，值修改时发送信号
	def __init__(self,parent=None,rgba=(255,50,50,255),hasAlpha=True):
		super().__init__(parent)
		self.setCursor(Qt.PointingHandCursor)
		self.setMinimumSize(32,32)
		self.__color=QColor(*rgba)
		self.__hasAlpha=hasAlpha
		self.__SetColor()
	def Set_Color(self,color):#color可为元组，如(255,128,64)
		if(not isinstance(color,QColor)):
			if(not self.__hasAlpha):
				color=color[:3]
			color=QColor(*color)
		self.__color=color
		self.__SetColor()
		self.valueChanged.emit(self.Get_Color())#值修改时发送信号
	def Get_Color(self):#返回rgba
		col=self.__color
		return (col.red(),col.green(),col.blue(),col.alpha())
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

