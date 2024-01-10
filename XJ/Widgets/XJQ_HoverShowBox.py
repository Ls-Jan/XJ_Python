

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPropertyAnimation,QRect


class XJQ_HoverShowBox(QWidget):#悬浮显示型容器
	'''
		悬浮显示型容器，在鼠标位于容器上方时动画显示容器元素
		配合牛皮癣XJQ_LocateBox将获得更好的用户体验
	'''
	def __init__(self,content=None,*,
			duration=1000,#动画持续时间
			direction=Qt.AlignLeft,):#出现方向(九向)，正中缩放，一般建议只用水平竖直四向

		super().__init__()
		if(content==None):
			content=QWidget()
		content.setParent(self)
		self.__content=content
		self.__animate=QPropertyAnimation()
		# setDuration(duration)
		# setTargetObject
		self.setAttribute(Qt.WA_Hover)#使用该属性即可
	def Set_Content(self,content):
		content.setParent(self)
		self.__content.setParent(None)
		self.__content=content
	# def enterEvent(self,event):

	# def leaveEvent(self,event):


from PyQt5.QtWidgets import QApplication,QWidget,QPushButton
from PyQt5.QtCore import QPropertyAnimation,QRect,QTimer

if True:
	app = QApplication([])

	wid=XJQ_HoverShowBox()
	# wid=QWidget()
	wid.show()
	app.exec_()


