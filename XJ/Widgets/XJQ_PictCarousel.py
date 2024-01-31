import os
import cv2
import numpy as np
from PIL import Image#动图类型的，cv2处理不了，只能借助PIL.Image

from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QFrame
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .XJQ_Icon import *
from .XJQ_SwitchBtn import *
from ..Functions import GetRealPath

# __all__=['XJQ_PictCarousel']

class XJQ_PictCarouselOpUI(QFrame):
	__play=None
	__index=None
	__slider=None
	def __init__(self,parent):
		super().__init__()
		play=XJQ_SwitchBtn()
		index=QLabel()
		slider=QSlider(Qt.Horizontal)
		# play.valueChanged.connect()
		slider.valueChanged.connect(self.Set_Index)
		hbox=QHBoxLayout(self)
		hbox.addWidget(play)
		hbox.addWidget(index)
		hbox.addWidget(slider,1)
		vbox=QVBoxLayout(parent)
		vbox.addStretch(1)
		vbox.addWidget(self)
		self.__slider=slider
		self.__index=index
		self.__play=play
		self.setStyleSheet('.XJQ_PictCarouselOpUI{background:rgba(0,0,0,160)}')
	def Set_Index(self,index=None,count=None):
		if(count==None):
			count=self.__slider.maximum()
		if(index==None):
			index=self.__slider.value()
		self.__slider.setMaximum(count)
		self.__slider.setValue(index)
		self.__index.setText(f'{index+1}/{count+1}')
	def Opt_Pause(self,flag=True):
		self.__play.Opt_Switch(not flag)



class XJQ_PictCarousel(QWidget):#图片轮播
	'''
		图片轮播，图片数量过多容易爆内存，不能作为视频播放器使用(Qt有它自己的原生播放器)
		其主要作用是作为视频/动图的预览，用于快速调整分辨率以及播放速率
	'''
	__frames=None
	__pict=None
	__index=None
	__scale=1
	__timerPlay=None
	__timerLoop=None
	def __init__(self):
		super().__init__()
		self.__opui=XJQ_PictCarouselOpUI(self)
		self.__frames=[]
		self.__index=0
		self.__pict=None
		self.__scale=1
		self.__timerPlay=QTimer()
		self.__timerLoop=QTimer()
		self.__timerPlay.timeout.connect(self.__Update)
		self.__timerLoop.timeout.connect(self.__NextLoop)
		self.__timerLoop.setSingleShot(True)
		# QVBoxLayout()
		self.Set_Duration(10)
		self.Set_Interval(500)
	def Opt_StartMovie(self):
		self.__timerPlay.start()
	def Opt_StopMovie(self):
		self.__timerLoop.stop()
		self.__timerPlay.stop()
	def Set_Duration(self,duration):
		self.__timerPlay.stop()
		self.__timerPlay.setInterval(duration)
		self.__timerPlay.start()
	def Set_Interval(self,interval):
		self.__timerLoop.stop()
		self.__timerLoop.setInterval(interval)
		self.__timerPlay.start()
	def Set_Index(self,index):
		self.__index=index
	def Set_Scale(self,scale):
		self.__scale=scale
		self.update()
	def Set_Frames(self,lst):
		self.__frames=lst
		self.update()
	def paintEvent(self,event):
		ptr=QPainter(self)
		if(self.__pict):
			size=self.__pict.size()*self.__scale
			ptr.drawPixmap(0,0,size.width(),size.height(),self.__pict)
	def __Update(self):
		if(self.__index<len(self.__frames)):
			pict=self.__frames[self.__index]
			if(not isinstance(pict,QPixmap)):
				pict=None
			self.__index+=1
			self.__pict=pict
			self.update()
		else:
			self.__index=0
			self.__timerPlay.stop()
			self.__timerLoop.start()
	def __NextLoop(self):
		self.__Update()
		self.__timerPlay.start()
	def leaveEvent(self,event):
		pass
	def enterEvent(self,event):
		print("EEE")




