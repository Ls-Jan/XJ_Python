
__version__='1.0.0'
__author__='Ls_Jan'

from .XJQ_AnimateShowHideBox import *
from .XJQ_PlayBar import *

from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QFrame,QWidget,QLabel
from PyQt5.QtCore import Qt,QTimer,pyqtSignal
from PyQt5.QtGui import QPixmap,QColor,QPainter

__all__=['XJQ_PictCarousel']

class XJQ_PictCarousel(QWidget):#图片轮播
	'''
		图片轮播，图片数量过多容易爆内存，不能作为视频播放器使用(Qt有它自己的原生播放器)
		其主要作用是作为视频/动图的预览，用于快速调整分辨率以及播放速率
	'''
	__pb=None
	__shBox=None
	__frames=None
	__pict=None
	__scale=1
	def __init__(self,loop=True):
		super().__init__()
		pb=XJQ_PlayBar()
		pb.valueChanged.connect(self.__Update)
		pb.Set_SliderStep(1)
		shBox=XJQ_AnimateShowHideBox(content=pb)
		self.__pb=pb
		self.__shBox=shBox
		self.__frames=[]
		self.__pict=None
		self.__scale=1
		self.__loop=loop
		vbox=QVBoxLayout(self)
		vbox.addStretch(1)
		vbox.addWidget(shBox)
	def Get_IsActive(self):
		return self.__pb.Get_IsActive()
	def Set_SliderStep(self,step):
		self.__pb.Set_SliderStep(step)
	def Set_Loop(self,interval=None,flag=None):
		self.__pb.Set_Loop(interval,flag)
	def Set_Duration(self,duration):
		self.__pb.Set_Duration(duration)
	def Set_Index(self,index):
		self.__pb.Set_Index(index)
	def Set_Scale(self,scale):
		self.__scale=scale
		self.update()
	def Set_Frames(self,lst):
		self.__frames=lst
		self.__pb.Set_Index(total=len(lst)-1)
		self.update()
	def Opt_Play(self,flag=True):
		self.__pb.Opt_Play(flag)
	def __Update(self,index,isNext):
		self.__pict=self.__frames[index]
		self.update()
	def __NextLoop(self):
		self.__pb.Set_Index(0)
		self.__pb.Opt_Play(True)
	def leaveEvent(self,event):
		self.__shBox.hide()
	def enterEvent(self,event):
		self.__shBox.show()
	def wheelEvent(self,event):
		if(event.angleDelta().y()<0):
			self.__scale*=0.9
		else:
			self.__scale*=1.1
	def paintEvent(self,event):
		ptr=QPainter(self)
		if(self.__pict):
			size=self.__pict.size()*self.__scale
			LT=(self.size()-size)/2
			ptr.drawPixmap(LT.width(),LT.height(),size.width(),size.height(),self.__pict)




