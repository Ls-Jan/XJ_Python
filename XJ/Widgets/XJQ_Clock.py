
__version__='1.0.0'
__author__='Ls_Jan'

from .XJQ_SwitchBtn import XJQ_SwitchBtn
from .XJQ_PureColorIconButton import XJQ_PureColorIconButton
from .XJQ_LocateBox import XJQ_LocateBox
from .XJQ_AnimateShowHideBox import XJQ_AnimateShowHideBox
from ..Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QLabel,QWidget
from PyQt5.QtCore import Qt,pyqtSignal,QTimer
import time

__all__=['XJQ_Clock']

class OperationUI:
	'''
		很简单的UI，只为XJQ_Clock服务
	'''
	btnPlay=None
	btnQuit=None
	def __init__(self,parent,iconPause:str=GetRealPath('../Icons/暂停.png'),iconPlay:str=GetRealPath('../Icons/播放.png'),iconQuit:str=GetRealPath('../Icons/停止.png')):
		btnPlay=XJQ_SwitchBtn(XJQ_PureColorIconButton(iconPlay),XJQ_PureColorIconButton(iconPause))
		btnQuit=XJQ_PureColorIconButton(iconQuit)

		wid=QWidget()
		lbox=XJQ_LocateBox(wid)
		lbox.Opt_AddWidget(btnPlay,Qt.AlignCenter)
		lbox.Opt_AddWidget(btnQuit,Qt.AlignVCenter|Qt.AlignRight,(0,0))
		shbox=XJQ_AnimateShowHideBox(parent)
		shbox.Set_Content(wid)
		shbox.setStyleSheet('.XJQ_AnimateShowHideBox{background:rgba(0,0,0,128)}')
		self.btnPlay=btnPlay
		self.btnQuit=btnQuit
		self.__parent=parent
		self.__shbox=shbox
		self.resize()
		self.hide()
	def resize(self):
		size=self.__parent.size()
		self.__shbox.resize(size)
		size=size.boundedTo(size.transposed())#最小正方形
		self.btnPlay.resize(size/1.2)
		self.btnQuit.resize(size/1.6)
	def show(self):
		self.resize()
		if(not (self.btnPlay.isHidden() and self.btnQuit.isHidden())):
			self.__shbox.show()
	def hide(self):
		self.__shbox.hide()

class XJQ_Clock(QLabel):
	'''
		格式自定，文本样式自定，行为自定，内容自定，
		鼠标悬浮时显示操作按钮(可禁用)
	'''
	pause=pyqtSignal(bool)#时钟暂停和继续时触发
	quit=pyqtSignal()#退出时钟时触发
	__timer=None
	__txFunc=None
	__opui=None

	def __init__(self,
			  interval:int=0.1,
			  uiPausePlay:bool=True,
			  uiQuit:bool=True):
		'''
			interval为刷新间隔(s)，默认0.1秒
			uiPausePlay为假则不显示暂停继续按钮
			uiQuit为假则不显示退出按钮
		'''
		super().__init__()
		timer=QTimer()
		timer.timeout.connect(self.__Update)
		self.resize(250,60)
		self.setStyleSheet('font-size:40px')
		self.setAlignment(Qt.AlignCenter)
		# self.setAttribute(Qt.FramelessWindowHint|Qt.ToolTip)

		opui=OperationUI(self)
		opui.btnPlay.setVisible(uiPausePlay)
		opui.btnQuit.setVisible(uiQuit)
		opui.btnPlay.valueChanged.connect(self.Opt_Continue)
		opui.btnQuit.clicked.connect(self.Opt_Quit)
		self.__timer=timer
		self.__txFunc=lambda:time.strftime("%H:%M:%S")
		self.__opui=opui
		self.Set_Interval(interval)
		self.__Update()
	def Get_IsRunning(self):
		'''
			判断是否正在运行
		'''
		return self.__timer.isActive()
	def Set_ContentFunc(self,func):
		'''
			设置用于内容更新的回调函数，该函数返回字符串作为文本内容
			函数func无参
		'''
		self.__txFunc=func
		self.__Update()
	def Set_Interval(self,interval:float):
		'''
			设置刷新间隔(s)
		'''
		isActive=self.__timer.isActive()
		self.__timer.stop()
		self.__timer.setInterval(interval*1000)
		if(isActive):
			self.__timer.start()
	def Opt_Quit(self):
		'''
			退出时钟
		'''
		self.Opt_Continue(False)
		self.close()
		self.quit.emit()
	def Opt_Continue(self,flag:bool=True,*,reverse:bool=False):
		'''
			运行时钟。当指定reverse时直接取反当前时钟状态
		'''
		if(reverse):
			flag=self.__timer.isActive()
		if(flag):
			self.__timer.start()
		else:
			self.__timer.stop()
		self.pause.emit(not flag)
		self.__opui.btnPlay.Opt_Switch(flag)
	def __Update(self):
		self.setText(self.__txFunc())
	def enterEvent(self,event):
		self.__opui.show()
	def leaveEvent(self,event):
		self.__opui.hide()


