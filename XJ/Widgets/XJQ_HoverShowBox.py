

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QPixmap


class XJQ_HoverShowBox(QWidget):#悬浮显示型容器
	'''
		悬浮显示型容器，在鼠标位于容器上方时动画显示容器元素
		配合牛皮癣XJQ_LocateBox将获得更好的用户体验
	'''
	def __init__(self,content=None,*,
			delay=0,#延迟显示
			interval=20,#动画刷新间隔
			pixel=10,#动画每帧平移
			direction=Qt.AlignLeft,#出现方向(八向)，一般建议只用水平竖直四向
			forward=True,):#正向滚动

		super().__init__()
		if(content==None):
			content=QWidget()
		content.setParent(self)
		self.__content=content

	def Set_Content(self,content):
		content.setParent(self)
		self.__content.setParent(None)
		self.__content=content




from PyQt5.QtWidgets import QApplication,QWidget,QPushButton
from PyQt5.QtCore import QPropertyAnimation,QRect,QTimer

if True:
	app = QApplication([])

	wid=QWidget()
	btn=QPushButton("ABC",wid)
	pa=QPropertyAnimation(btn,'geometry'.encode())
	btn.show()
	wid.show()
	wid.resize(400,400)
	def Func():
		pa.stop()
		if(btn.text()=='上'):
			rect=QRect(200,200,100,100)
			btn.setText('下')
		else:
			rect=QRect(200,50,50,50)
			btn.setText('上')
		pa.setEndValue(rect)
		pa.start()
	Func()

	btn.clicked.connect(Func)
	app.exec_()


