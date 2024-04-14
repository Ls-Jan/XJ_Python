
__version__='1.1.0'
__author__='Ls_Jan'

from ..XJQ_AnimateShowHideBox import XJQ_AnimateShowHideBox
from ..XJQ_PureColorIcon import XJQ_PureColorIcon
from ..XJQ_PlayBar import XJQ_PlayBar
from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager
from ...Functions.GetRealPath import GetRealPath

from typing import Union
from PyQt5.QtWidgets import QVBoxLayout,QWidget,QLabel
from PyQt5.QtGui import QPainter

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
	def __init__(self,*args,playBar:XJQ_PlayBar=None):
		'''
			不指定playBar时将生成默认的XJQ_PlayBar对象
		'''
		super().__init__(*args)
		pb=playBar if playBar else XJQ_PlayBar(True)
		pb.valueChanged.connect(self.__Update)
		pb.Set_SliderStep(1)
		hint=QLabel('x1.0')
		shBox_pb=XJQ_AnimateShowHideBox(content=pb)
		shBox_ht=XJQ_AnimateShowHideBox(content=hint,autoSize=True)
		shBox_ht.setParent(self)
		# shBox_ht.resize(500,500)
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
		self.setStyleSheet(GetRealPath('./styleSheet.qss'),None)
	def setStyleSheet(self,qss:str,name:str='Main'):
		'''
			name可选值为Main、ScaleHint、PlayBar。
			qss可为文件路径。
			特别的，如果name直接传None则加载qss中的复数个样式表
		'''
		sm=XJQ_StyleSheetManager()
		sm.setStyleSheet(qss,multi=name==None)
		qss=sm.styleSheet()
		if(name=='Main'):
			super().setStyleSheet(qss)
		elif(name=='ScaleHint'):
			self.__hint.setStyleSheet(qss)
		elif(name=='PlayBar'):
			self.__pb.setStyleSheet(qss)
		elif(name==None):
			for name,qss in sm.styleSheet(returnDict=True).items():
				self.setStyleSheet(qss,name)
	def Set_Icon(self,iconPlay:Union[XJQ_PureColorIcon,str]=None,iconPause:Union[XJQ_PureColorIcon,str]=None):
		'''
			设置播放停止按钮
		'''
		self.__pb.Set_Icon(iconPlay,iconPause)
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
	def Set_Loop(self,msec:int=None,flag:bool=None):
		'''
			设置循环播放，
			msec为每次播放之间的时间间隔(ms)
			flag为是否循环播放
		'''
		self.__pb.Set_Loop(msec,flag)
	def Set_Duration(self,msec:int):
		'''
			设置帧播放的时间间隔(ms)
		'''
		self.__pb.Set_Duration(msec)
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
			设置帧列表，数据为QPixmap
		'''
		self.__frames=lst
		self.__pict=None
		self.__pb.Set_Index(max=len(lst)-1)
		self.update()
	def Get_Frames(self):
		'''
			获取帧列表，数据为QPixmap
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


