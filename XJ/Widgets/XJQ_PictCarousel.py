
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
	__shBox_pb=None
	__shBox_ht=None
	__frames=None
	__pict=None
	__scale=1
	__hint=None
	def __init__(self,*args):
		super().__init__(*args)
		pb=XJQ_PlayBar()
		pb.valueChanged.connect(self.__Update)
		pb.Set_SliderStep(1)
		hint=QLabel('x1.0')
		shBox_pb=XJQ_AnimateShowHideBox(content=pb)
		shBox_ht=XJQ_AnimateShowHideBox(content=hint)
		shBox_ht.setParent(self)
		hint.setStyleSheet('font-size:30px;color:#000000;background:#88FFFFFF')
		self.__pb=pb
		self.__shBox_pb=shBox_pb
		self.__shBox_ht=shBox_ht
		self.__frames=[]
		self.__pict=None
		self.__scale=1
		self.__hint=hint
		self.Set_Scale(self.__scale)
		vbox=QVBoxLayout(self)
		vbox.addStretch(1)
		vbox.addWidget(shBox_pb)
	def Get_IsActive(self):
		'''
			判断是否播放中
		'''
		return self.__pb.Get_IsActive()
	def Set_SliderStep(self,step:int):
		'''
			设置播放条的步长
		'''
		self.__pb.Set_SliderStep(step)
	def Set_Loop(self,interval:int=None,flag:bool=None):
		'''
			设置循环播放，
			interval为每次播放之间的时间间隔(ms)
			flag为是否循环播放
		'''
		self.__pb.Set_Loop(interval,flag)
	def Set_Duration(self,duration:int):
		'''
			设置帧播放的时间间隔(ms)
		'''
		self.__pb.Set_Duration(duration)
	def Set_Index(self,index:int):
		'''
			设置当前帧索引
		'''
		self.__pb.Set_Index(index)
	def Set_Scale(self,scale:float):
		'''
			设置画面缩放比
		'''
		if(scale<0.1):
			scale=0.1
		elif(scale>10):
			scale=10
		self.__scale=scale
		self.__shBox_ht.show(immediate=True,autoHide=1000)
		self.__hint.setText(f'x{round(scale,1)}')
		self.update()
	def Set_Frames(self,lst:list):
		'''
			设置帧列表
		'''
		self.__frames=lst
		self.__pb.Set_Index(max=len(lst)-1)
		self.update()
	def Get_Frames(self):
		'''
			获取帧列表
		'''
		return self.__frames
	def Opt_Play(self,flag:bool=True):
		'''
			播放或者暂停
		'''
		self.__pb.Opt_Play(flag)

	def __Update(self,index,isNext):
		if(0<=index<len(self.__frames)):
			self.__pict=self.__frames[index]
			self.update()
	def leaveEvent(self,event):
		self.__shBox_pb.hide()
	def enterEvent(self,event):
		self.__shBox_pb.show()
	def wheelEvent(self,event):
		rate=0.9 if event.angleDelta().y()<0 else 1.1
		self.Set_Scale(self.__scale*rate)
	def paintEvent(self,event):
		ptr=QPainter(self)
		if(self.__pict):
			size=self.__pict.size()*self.__scale
			LT=(self.size()-size)/2
			ptr.drawPixmap(LT.width(),LT.height(),size.width(),size.height(),self.__pict)


