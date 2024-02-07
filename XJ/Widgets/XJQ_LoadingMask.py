
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QLabel
from PyQt5.QtGui import QMovie,QPixmap
from PyQt5.QtCore import QSize

__all__=['XJQ_LoadingMask']


class XJQ_LoadingMask(QLabel):#加载动画蒙版
	'''
		加载动画蒙版，遮蔽控件的不二之选，
		gif动画可以指定，文字也可以指定(文字是静态的，通常也不需要动态文字
		动画大小以及文字的颜色和大小均可指定，实在不满足可以设置样式表
	'''
	def __init__(self,filePath,parent=None,text="加载中...",size=(50,50)):
		super().__init__(parent)
		self.__lb_tx=QLabel()
		self.__lb_gif=QLabel()
		self.Set_Icon(size,filePath)
		self.Set_Hint(text,(0,255,255,192),20)
		self.setStyleSheet('''
			.XJQ_LoadingMask{
				background:rgba(0,0,0,224);
			}
		''')

		hbox1=QHBoxLayout()
		hbox2=QHBoxLayout()
		vbox=QVBoxLayout(self)
		hbox1.addStretch(1)
		hbox1.addWidget(self.__lb_gif)
		hbox1.addStretch(1)
		hbox2.addStretch(1)
		hbox2.addWidget(self.__lb_tx)
		hbox2.addStretch(1)
		vbox.addStretch(1)
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addStretch(1)
	def paintEvent(self,event):
		if(not self.parent()):
			return
		self.resize(self.parent().size())
		super().paintEvent(event)
	def Set_Hint(self,text=None,color=None,size=None):
		style=''
		if(size!=None):
			style+=f'font-size:{size}px;'
		if(color!=None):
			tx=""
			if(isinstance(color,tuple)):
				tx='rgba' if len(color)==4 else 'rgb'
			style+=f'color:{tx}{color};'
		if(text!=None):
			self.__lb_tx.setText(text)
		self.__lb_tx.setStyleSheet(style)
	def Set_Icon(self,size,path=None):
		if(path):
			#貌似这玩意儿会导致内存泄漏：https://blog.csdn.net/V10_x/article/details/135514227
			#但在PyQt中不知道有没有被优化掉(因为Python中的析构是通过引用数来控制的)
			#没心情去试它的析构条件，估摸着py的垃圾回收机制会好好干活
			mv=QMovie(path)
			mv.start()
		else:
			mv=self.__lb_gif.movie()
			if(not mv):
				return
		size=QSize(*size)
		if(mv.frameCount()):#动图的frame不为0
			mv.setScaledSize(size)
			self.__lb_gif.setMovie(mv)
		else:#静图，使用QPixmap
			#虽然QMovie也能打开静图，不知道搭错什么筋，没法调整大小
			pix=QPixmap(path).scaled(size)
			self.__lb_gif.setPixmap(pix)
