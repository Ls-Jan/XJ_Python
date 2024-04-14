
__version__='1.1.0'
__author__='Ls_Jan'

from .OperationUI import OperationUI
from ...Functions.GetRealPath import GetRealPath
from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt,pyqtSignal,QTimer
import time

__all__=['XJQ_Clock']

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
			  showBtnPausePlay:bool=True,
			  showBtnQuit:bool=True,
			  iconPause:str=GetRealPath('./暂停.png'),
			  iconPlay:str=GetRealPath('./播放.png'),
			  iconQuit:str=GetRealPath('./停止.png')):
		'''
			interval为刷新间隔(s)，默认0.1秒；
			showBtnPausePlay为假则不显示暂停继续按钮；
			showBtnQuit为假则不显示退出按钮；
		'''
		super().__init__()
		timer=QTimer()
		timer.timeout.connect(self.__Update)
		self.resize(250,60)
		self.setAlignment(Qt.AlignCenter)
		# self.setAttribute(Qt.FramelessWindowHint|Qt.ToolTip)

		opui=OperationUI(self,iconPause,iconPlay,iconQuit)
		opui.btnPlay.setVisible(showBtnPausePlay)
		opui.btnQuit.setVisible(showBtnQuit)
		opui.btnPlay.valueChanged.connect(self.Opt_Continue)
		opui.btnQuit.clicked.connect(self.Opt_Quit)
		self.__timer=timer
		self.__txFunc=lambda:time.strftime("%H:%M:%S")
		self.__opui=opui
		self.Set_Interval(interval)
		self.__Update()
		self.setStyleSheet(GetRealPath('./styleSheet.qss'),None)
	def setStyleSheet(self,qss:str,name:str='Main'):
		'''
			name可选值为Main、OpeartionUI。
			qss可为文件路径。
			特别的，如果name直接传None则加载qss中的复数个样式表
		'''
		sm=XJQ_StyleSheetManager()
		sm.setStyleSheet(qss,multi=name==None)
		qss=sm.styleSheet()
		if(name=='Main'):
			super().setStyleSheet(qss)
		elif(name=='OperationUI'):
			self.__opui.setStyleSheet(qss)
		elif(name==None):
			for name,qss in sm.styleSheet(returnDict=True).items():
				self.setStyleSheet(qss,name)
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


