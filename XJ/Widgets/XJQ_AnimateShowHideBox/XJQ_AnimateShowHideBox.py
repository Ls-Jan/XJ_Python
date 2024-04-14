
__version__='1.0.1'
__author__='Ls_Jan'

from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QGraphicsOpacityEffect,QFrame,QVBoxLayout,QWidget
from PyQt5.QtCore import QPropertyAnimation,Qt,QTimer

__all__=['XJQ_AnimateShowHideBox']

class XJQ_AnimateShowHideBox(QFrame):
	'''
		动画显隐容器，继承自QFrame是因为可能有调用setStyleSheet设置背景色的需要。
		附赠点击穿透，仅控件完全显示后才能响应鼠标事件

		一开始是不打算使用Box形式的，
		但后来发现显隐效果需要调用QWidget.setGraphicsEffect，
		如果不采用容器的方式的话实现动画效果势必调用目标控件的setGraphicsEffect方法，
		而这增加了耦合度以及不确定的开发风险，(因为setGraphicsEffect会覆盖上一次的调用)
	'''
	def __init__(self,
			  parent:QWidget=None,
			  content:QWidget=None,
			  allowTransparent:bool=True,
			  autoSize:bool=False):
		'''
			当allowTransparent为真时，仅控件完全显示后才可点击，
			该值置假时控件在显隐过程中可点击，可将此作为遮罩的延迟关闭(仅遮罩完全消失后才能进一步操作)；
			adjustSize为自动调整大小，当该值为真时会将动画盒子的大小设置为获取内容物的sizeHint值
		'''
		super().__init__(parent)
		timerHide=QTimer()
		timerHide.setSingleShot(True)
		timerHide.timeout.connect(self.hide)
		vbox=QVBoxLayout(self)
		vbox.setContentsMargins(0,0,0,0)
		self.__trans=allowTransparent
		self.__wid=None
		self.__autoSize=False
		self.__effect=QGraphicsOpacityEffect()
		self.__animate=QPropertyAnimation(self.__effect,b'opacity')
		self.__effect.setOpacity(1)
		self.__animate.setDuration(300)
		self.__animate.finished.connect(self.__AnimateFinish)
		self.__timerHide=timerHide
		self.Set_Content(content,autoSize)
		self.setGraphicsEffect(self.__effect)
	def Set_Content(self,wid:QWidget=None,autoSize:bool=False):
		'''
			设置内容物(为None则清空)。
			adjustSize为自动调整大小，当该值为真时会将动画盒子的大小设置为获取内容物的sizeHint值
		'''
		vbox=self.layout()
		if(self.__wid):
			vbox.removeWidget(self.__wid)
		self.__wid=wid
		if(wid):
			vbox.addWidget(wid)
		self.__autoSize=autoSize
	def Get_Content(self):
		'''
			获取内容物
		'''
		return self.__wid
	def Set_Duration(self,duration:int):
		'''
			设置显隐动画间隔(ms)
		'''
		self.__animate.setDuration(duration)
	def show(self,immediate:bool=False,autoHide:int=0):
		'''
			如果immediate为真那么直接显示。
			新增：autoHide用于自动隐藏，在控件完全显示后经过一段时间将自动动画隐藏，单位为ms
		'''
		super().show()
		self.__animate.stop()
		if(immediate):
			self.__effect.setOpacity(1)
		else:
			self.__animate.setEndValue(1)
			self.__animate.start()
		if(autoHide>0):
			timerHide=self.__timerHide
			timerHide.stop()
			timerHide.setInterval((self.__animate.duration() if not immediate else 0)+autoHide)
			timerHide.start()
	def hide(self,immediate:bool=False):
		'''
			如果immediate为真那么直接隐藏
		'''
		if(self.__trans):
			self.setAttribute(Qt.WA_TransparentForMouseEvents,True)
		self.__animate.stop()
		if(immediate):
			self.__effect.setOpacity(0)
		else:
			self.__animate.setEndValue(0)
			self.__animate.start()
	def paintEvent(self,event):
		if(self.__wid!=None and self.__autoSize):
			self.resize(self.__wid.sizeHint())
		return super().paintEvent(event)
	def __AnimateFinish(self):
		if(self.__effect.opacity()==0):
			super().hide() 
		else:
			self.setAttribute(Qt.WA_TransparentForMouseEvents,False)



