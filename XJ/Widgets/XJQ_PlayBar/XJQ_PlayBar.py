
__version__='1.1.0'
__author__='Ls_Jan'


from ..XJQ_SwitchBtn import XJQ_SwitchBtn
from ..XJQ_PureColorIconButton import XJQ_PureColorIconButton
from ..XJQ_PureColorIcon import XJQ_PureColorIcon
from ..XJQ_Slider import XJQ_Slider
from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager
from ...Functions.GetRealPath import GetRealPath

from typing import Union
from PyQt5.QtWidgets import QHBoxLayout,QFrame,QLabel
from PyQt5.QtCore import Qt,QTimer,pyqtSignal
from PyQt5.QtGui import QColor

__all__=['XJQ_PlayBar']

class XJQ_PlayBar(QFrame):#播放条
	'''
		播放条，以帧为单位，不单独使用
	'''
	valueChanged=pyqtSignal(int,bool)#增加一个bool是为了特定场合下减少判断罢了，如果是值+1那么bool为真
	valueStart=pyqtSignal()#播放开始时发出信号(启用Loop时生效)
	valueEnd=pyqtSignal()#播放到底时发出信号
	indexFormat=lambda self,index,total:f'{index+1}/{total+1}'

	__widPlay=None
	__widIndex=None
	__widSlider=None
	__timerPlay=None
	__timerLoop=None
	__timerPause=500#操作滚动条时短暂暂停(贤者时间
	__loop=None
	def __init__(self,loop=True,iconPlay:Union[XJQ_PureColorIcon,str]=GetRealPath('./播放.png'),iconPause:Union[XJQ_PureColorIcon,str]=GetRealPath('./暂停.png')):
		super().__init__()
		widPlay=XJQ_SwitchBtn(XJQ_PureColorIconButton(),XJQ_PureColorIconButton())
		widIndex=QLabel("0/0")
		widSlider=XJQ_Slider(Qt.Horizontal)
		timerPlay=QTimer()
		timerLoop=QTimer()
		timerPause=QTimer()
		widSlider.setInvertedControls(True)
		widSlider.sliderPressed.connect(lambda:self.__TempPause(False))
		widSlider.sliderReleased.connect(self.__TempPause)
		widSlider.sliderWheeled.connect(self.__TempPause)
		widSlider.Set_HandleWidth(20)
		widSlider.Set_Color(sub=QColor(32,255,32,160))
		widSlider.setRange(0,0)
		timerLoop.setSingleShot(True)
		timerPause.setSingleShot(True)
		timerPause.setInterval(self.__timerPause)
		widPlay.valueChanged.connect(self.Opt_Play)
		widPlay.setFixedSize(32,32)#锁大小
		widSlider.valueChanged.connect(self.Set_Index)
		timerPlay.timeout.connect(self.__NextFrame)
		timerLoop.timeout.connect(self.__NextLoop)
		timerPause.timeout.connect(self.__TempPauseEnd)

		hbox=QHBoxLayout(self)
		hbox.addWidget(widPlay)
		hbox.addWidget(widIndex,1)
		hbox.addWidget(widSlider,20)
		self.__widPlay=widPlay
		self.__widIndex=widIndex
		self.__widSlider=widSlider
		self.__timerPlay=timerPlay
		self.__timerLoop=timerLoop
		self.__timerPause=timerPause
		self.__loop=loop
		self.Set_Icon(iconPlay,iconPause)
		self.Set_Duration(50)
		self.Set_Loop(250)
		self.setStyleSheet(GetRealPath('./styleSheet.qss'),None)
	def setStyleSheet(self,qss:str,name:str='Main'):
		'''
			name可选值为Main、Index。
			qss可为文件路径。
			特别的，如果name直接传None则加载qss中的复数个样式表(此时qss可为文件路径)
		'''
		sm=XJQ_StyleSheetManager()
		sm.setStyleSheet(qss,multi=name==None)
		qss=sm.styleSheet()
		if(name=='Main'):
			super().setStyleSheet(qss)
		elif(name=='Index'):
			self.__widIndex.setStyleSheet(qss)
		elif(name==None):
			for name,qss in sm.styleSheet(returnDict=True).items():
				self.setStyleSheet(qss,name)
	def Get_IsActive(self):
		'''
			判断是否在播放
		'''
		return self.__widPlay.Get_IsON()
	def Set_Icon(self,iconPlay:Union[XJQ_PureColorIcon,str]=None,iconPause:Union[XJQ_PureColorIcon,str]=None):
		'''
			设置播放停止按钮
		'''
		for item in [(self.__widPlay.Get_BtnON(),iconPlay),(self.__widPlay.Get_BtnOFF(),iconPause)]:
			if(iconPlay):
				try:
					item[0].Set_Icon(item[1])
				except:
					pass
	def Set_Duration(self,duration:int):
		'''
			设置每帧的持续时间(ms)
		'''
		self.__timerPlay.setInterval(duration)
	def Set_Loop(self,interval:int=None,flag:bool=None):
		'''
			设置循环播放，
			interval为每次播放之间的时间间隔(ms)
			flag为是否循环播放
		'''
		if(flag!=None):
			self.__loop=flag
		if(interval!=None):
			isActive=self.__timerLoop.isActive()
			self.__timerLoop.stop()
			self.__timerLoop.setInterval(interval)
			if(isActive):
				self.__timerLoop.start()
	def Set_SliderStep(self,step:int):
		'''
			设置播放条的步长
		'''
		self.__widSlider.setPageStep(step)
	def Set_Index(self,index:int=None,max:int=None):
		'''
			设置当前值以及最大值，
			设置后当前值发生变化则返回真
		'''
		slider=self.__widSlider
		if(max==None):
			max=slider.maximum()
		if(index==None):
			index=slider.value()
		slider.setMinimum(0 if max>=0 else -1)
		v0=slider.value()
		slider.setMaximum(max)
		v1=slider.value()
		slider.setValue(index)
		v2=slider.value()
		if(max<0):
			self.__widIndex.setText(self.indexFormat(-1,-1))
		else:
			self.__widIndex.setText(self.indexFormat(v2,max))
		self.valueChanged.emit(v2,v1+1==v2)
		return v0!=v2
	def Opt_Play(self,flag:bool=True):
		'''
			播放或者暂停
		'''
		self.__timerLoop.stop()
		self.__timerPause.stop()
		if(flag):
			if(self.__widSlider.maximum()>=0):
				if(self.__widSlider.value()==self.__widSlider.maximum()):
					self.__NextLoop()
				else:
					self.__timerPlay.start()
		else:
			self.__timerPlay.stop()
		self.__widPlay.Opt_Switch(flag)

	def __NextFrame(self):
		if(self.Set_Index(self.__widSlider.value()+1)):
			self.update()
		if(self.__widSlider.value()==self.__widSlider.maximum()):
			self.valueEnd.emit()
			self.__timerPlay.stop()
			if(self.__loop):
				self.__timerLoop.start()
			else:
				self.__timerPlay.stop()
				self.__widPlay.Opt_Switch(False)
	def __NextLoop(self):
		self.Set_Index(0)
		self.valueStart.emit()
		self.__timerPlay.start()
	def __TempPause(self,temp=True):
		self.__timerLoop.stop()
		self.__timerPlay.stop()
		self.__timerPause.stop()
		if(temp):
			self.__timerPause.start()
	def __TempPauseEnd(self):
		if(self.Get_IsActive()):
			self.Opt_Play()
	def wheelEvent(self,event):#阻止滚轮事件向上传递
		event.accept()
