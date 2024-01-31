from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from XJ.Functions.GetScreensArea import *

class _BorderShow(QWidget):
	def __init__(self,win):
		super().__init__()
		area=GetScreensArea(True)
		self.__win=win
		self.setGeometry(area)
		self.setAttribute(Qt.WA_TranslucentBackground, True)#透明背景。该属性要和Qt.FramelessWindowHint配合使用，单独用的话不生效
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.ToolTip|Qt.WindowStaysOnTopHint)#测试发现Qt.WindowStaysOnTopHint可省略
	def showEvent(self,event):
		self.__win.activateWindow()#设置活跃窗口：https://blog.csdn.net/qq_42281306/article/details/96423691
	def paintEvent(self,event):
		ptr=QPainter(self)
		ptr.fillRect(0,0,500,500,QColor(255,0,0))

class _ContentBox(QWidget):#它唯一作用就是将光标置为ArrowCursor
	def __init__(self):
		super().__init__()
		self.__content=QWidget(self)
	def Set_Content(self,content):
		if(not content):
			content=QWidget()
		content.setParent(self)
		content.resize(self.size())
		content.show()
		self.__content.hide()
		self.__content.setParent(None)
		self.__content=content
	def resizeEvent(self,event):
		self.__content.resize(event.size())
	def enterEvent(self,event):
		self.setCursor(Qt.ArrowCursor)

class XJQ_FloatyWinBox(QWidget):#悬浮窗容器
	def __init__(self):
		super().__init__()
		contentBox=_ContentBox()
		vbox=QVBoxLayout(self)
		vbox.addWidget(contentBox)
		self.__vbox=vbox
		self.__margin=10
		self.__contentBox=contentBox
		self.Set_Margin(self.__margin)
		self.setMouseTracking(True)
	def Set_Content(self,content):
		self.__contentBox.Set_Content(content)
	def Set_Margin(self,margin):
		margin=(margin,)*4
		self.__vbox.setContentsMargins(*margin)
	def mouseMoveEvent(self,event):
		m2=self.__margin*2
		m4=m2*2
		size=self.rect().size()-QSize(1,1)
		pos=event.pos()
		limL=m2
		limR=size.width()-m4
		limT=m2
		limB=size.height()-m4
		line=''
		if(pos.x()<limL):
			line+='L'
		elif(pos.x()>limR):
			line+='R'
		if(pos.y()<limT):
			line+='T'
		elif(pos.y()>limB):
			line+='B'
		if(line=='L' or line=='R'):
			cursor=Qt.SizeHorCursor#水平
		elif(line=='T' or line=='B'):
			cursor=Qt.SizeVerCursor#竖直
		elif(line=='LT' or line=='RB'):
			cursor=Qt.SizeFDiagCursor#左上右下
		elif(line=='LB' or line=='RT'):
			cursor=Qt.SizeBDiagCursor#左下右上
		else:
			cursor=Qt.ArrowCursor#箭头
		self.setCursor(cursor)
		# print(,event.pos())
		print(line)
# 	def resizeEvent(self,event):
# 		print("resizeEvent:",event.size())
# 		# self.resize(QSize(150,150))
# 	def resize(self,*size):
# 		print("resize:",size)
# 		super().resize(*size)
# 	def setGeometry(self,*rect):
# 		print("setGeometry:",rect)
# 		super().setGeometry(*rect)

if True:
	app = QApplication([])

	# win=__WinBack()
	# win.show()
	# win.resize(500,300)
	# app.exec_()
	
	# content=QFrame()
	# content.setStyleSheet('background:#FF0000')
	win=XJQ_FloatyWinBox()
	win.show()
	win.resize(500,300)
	t=QPushButton("ABC")
	win.Set_Content(t)
	app.exec_()

	win=QWidget()
	t=Test("ABC")
	vbox=QVBoxLayout(win)
	vbox.addWidget(t)
	win.show()
	win.resize(300,300)

	app.exec_()
