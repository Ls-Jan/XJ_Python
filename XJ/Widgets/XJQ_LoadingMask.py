
__version__='1.0.0'
__author__='Ls_Jan'

from typing import Union
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QLabel
from PyQt5.QtGui import QMovie,QPixmap, QShowEvent
from PyQt5.QtCore import QSize

__all__=['XJQ_LoadingMask']


class XJQ_LoadingMask(QLabel):#加载动画蒙版
	'''
		加载动画蒙版，遮蔽控件的不二之选，
		gif动画可以指定，文字也可以指定(文字是静态的，通常也不需要动态文字
		动画大小以及文字的颜色和大小均可指定，实在不满足可以设置样式表。
		额外的，即使调用setParent更改父控件也不会影响正常使用
	'''
	def __init__(self,
			  parent=None,
			  filePath:str=None,
			  text:str="加载中...",
			  iconSize:tuple=(64,64)):
		'''
			filePath为动图路径
			iconSize为动图大小
			text为额外的文本提示
		'''
		super().__init__(parent)
		self.__lb_tx=QLabel()
		self.__lb_gif=QLabel()
		self.Set_Icon(iconSize,filePath)
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
	def showEvent(self,event):
		mv=self.__lb_gif.movie()
		if(mv):
			mv.start()
		self.raise_()
		return super().showEvent(event)
	def hideEvent(self,event):
		mv=self.__lb_gif.movie()
		if(mv):
			mv.stop()
		return super().hideEvent(event)
	def Set_Hint(self,text:str=None,color:tuple=None,size:int=None):
		'''
			设置文本。
			color和size以样式表的方式生效
		'''
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
	def Set_Icon(self,iconSize:Union[QSize,tuple]=None,path:str=None):
		'''
			设置图标
		'''
		if(isinstance(iconSize,tuple)):
			iconSize=QSize(*iconSize)
		elif(iconSize==None):
			mv=self.__lb_gif.movie()
			pix=self.__lb_gif.pixmap()
			if(mv):
				iconSize=mv.scaledSize()
			elif(pix):
				iconSize=pix.size()
			else:
				iconSize=QSize(64,64)
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
		if(mv.frameCount()):#动图的frame不为0
			mv.setScaledSize(iconSize)
			self.__lb_gif.setMovie(mv)
		else:#静图，使用QPixmap
			#虽然QMovie也能打开静图，不知道搭错什么筋，没法调整大小
			pix=QPixmap(path).scaled(iconSize)
			self.__lb_gif.setPixmap(pix)

	def paintEvent(self,event):
		if(not self.parent()):
			return
		self.resize(self.parent().size())
		super().paintEvent(event)

