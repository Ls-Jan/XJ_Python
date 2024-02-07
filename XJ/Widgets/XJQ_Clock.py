
__version__='1.0.0'
__author__='Ls_Jan'

from .XJQ_MouseTrigger import *
from .XJQ_Icon import *
from .XJQ_LocateBox import *
from .XJQ_AnimateShowHideBox import *
from .XJQ_IconButton import *
from ..Functions.GetRealPath import *

from PyQt5.QtWidgets import QLabel,QFrame,QPushButton,QStackedLayout
from PyQt5.QtCore import Qt,QObject,QRect,pyqtSignal,QEvent,QTimer
import time

__all__=['XJQ_Clock']


class XJQ_ClockOpUI:
	btnPause=GetRealPath('./icons/暂停.png')
	btnPlay=GetRealPath('./icons/播放.png')
	btnQuit=GetRealPath('./icons/停止.png')
	btnPausePlay=None
	def __init__(self,parent):
		btnPause=XJQ_IconButton(self.btnPause)
		btnPlay=XJQ_IconButton(self.btnPlay)
		btnQuit=XJQ_IconButton(self.btnQuit)
		btnPausePlay=QWidget()
		btnPausePlay.setMinimumSize(1,1)#离谱，最小宽被锁160，最小高也被安排了一个值，被埋雷了

		stk=QStackedLayout(btnPausePlay)
		stk.addWidget(btnPause)
		stk.addWidget(btnPlay)
		btnPause.clicked.connect(lambda:stk.setCurrentIndex(1))
		btnPlay.clicked.connect(lambda:stk.setCurrentIndex(0))
		stk.setCurrentIndex(0)
		btnPausePlay.show()

		wid=QWidget()
		lbox=XJQ_LocateBox(wid)
		lbox.Opt_AddWidget(btnPausePlay,Qt.AlignCenter)
		lbox.Opt_AddWidget(btnQuit,Qt.AlignVCenter|Qt.AlignRight,(0,0))
		lbox.show()
		shbox=XJQ_AnimateShowHideBox(parent)
		shbox.Set_Content(wid)
		shbox.setStyleSheet('.XJQ_AnimateShowHideBox{background:rgba(0,0,0,128)}')
		self.btnPause=btnPause
		self.btnPlay=btnPlay
		self.btnQuit=btnQuit
		self.btnPausePlay=btnPausePlay
		self.__parent=parent
		self.__shbox=shbox
		self.resize()
	def resize(self):
		size=self.__parent.size()
		self.__shbox.resize(size)
		size=size.boundedTo(size.transposed())#最小正方形
		self.btnPausePlay.resize(size/1.2)
		self.btnQuit.resize(size/2)
	def show(self):
		self.resize()
		if(not (self.btnPausePlay.isHidden() and self.btnQuit.isHidden())):
			self.__shbox.show()
	def hide(self):
		self.__shbox.hide()




class XJQ_Clock(QLabel):#置顶时钟，格式自定，样式自定，行为自定，内容自定
	pause=pyqtSignal(bool)#时钟暂停和继续时触发
	quit=pyqtSignal()#退出时钟时触发
	__timer=None
	__txFunc=None
	__opui=None
	def __init__(self,interval=0.1,uiPausePlay=True,uiQuit=True):#默认0.1秒更新显示内容
		super().__init__()
		timer=QTimer()
		timer.setInterval(interval*1000)
		timer.timeout.connect(self.__Update)
		timer.start()
		self.resize(300,100)
		# self.resize(500,200)
		self.setStyleSheet('font-size:40px')
		# self.setStyleSheet('font-size:30px')
		self.setAlignment(Qt.AlignCenter)
		# self.setAttribute(Qt.FramelessWindowHint|Qt.ToolTip)

		opui=XJQ_ClockOpUI(self)
		opui.btnPausePlay.setVisible(uiPausePlay)
		opui.btnQuit.setVisible(uiQuit)
		opui.btnQuit.clicked.connect(lambda:print("Quit"))
		opui.btnPause.clicked.connect(lambda:print("Pause"))
		opui.btnPlay.clicked.connect(lambda:print("Play"))
		mt=XJQ_MouseTrigger(self)
		mt.Opt_AddRange('OP',(0,0),(1.0,1.0))
		mt.enter.connect(self.__Trigger)
		self.__timer=timer
		self.__txFunc=lambda:time.strftime("%H:%M:%S")
		self.__opui=opui
	def Get_IsRunning(self):
		return self.__timer.isActive()
	def Set_ContentFunc(self,func):#设置用于内容更新的回调函数，该函数返回字符串作为文本内容
		self.__txFunc=func
		self.__Update()
	def Opt_Pause(self,flag=True,reverse=False):#暂停/继续时钟
		if(reverse):
			flag=self.__timer.isActive()
		if(flag):
			self.__timer.stop()
			self.pause.emit(True)
		else:
			self.__timer.start()
			self.pause.emit(False)
	def Opt_Quit(self):#退出时钟
		self.Opt_Pause(True)
		self.close()
	def __Trigger(self,name,enter):
		if(enter):
			self.__opui.show()
		else:
			self.__opui.hide()
	def __Update(self):
		self.setText(self.__txFunc())

from PyQt5.QtWidgets import QApplication,QPushButton,QWidget,QLabel
from PyQt5.QtCore import QRect

if True:
	app = QApplication([])

	ck=XJQ_Clock()
	ck.show()

	app.exec_()




