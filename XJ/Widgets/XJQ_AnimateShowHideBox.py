
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtWidgets import QGraphicsOpacityEffect,QFrame,QVBoxLayout,QWidget
from PyQt5.QtCore import QPropertyAnimation,Qt

__all__=['XJQ_AnimateShowHideBox']

class XJQ_AnimateShowHideBox(QFrame):
	'''
		动画显隐容器，继承自QFrame是因为可能有调用setStyleSheet设置背景色的需要
		附赠点击穿透，仅控件完全显示后才能响应鼠标事件

		一开始是不打算使用Box形式的，
		但后来发现显隐效果需要调用QWidget.setGraphicsEffect，
		如果不采用容器的方式的话实现动画效果势必调用目标控件的setGraphicsEffect方法，
		而这增加了耦合度以及不确定的开发风险，(因为setGraphicsEffect会覆盖上一次的调用)
	'''
	def __init__(self,parent=None,content=None,allowTransparent=True):
		'''
			当allowTransparent为真时，仅控件完全显示后才可点击，
			该值置假时控件在显隐过程中可点击，可将此作为遮罩的延迟关闭(仅遮罩完全消失后才能进一步操作)
		'''
		super().__init__(parent)
		vbox=QVBoxLayout(self)
		vbox.setContentsMargins(0,0,0,0)
		self.__trans=allowTransparent
		self.__wid=None
		self.__effect=QGraphicsOpacityEffect()
		self.__animate=QPropertyAnimation(self.__effect,b'opacity')
		self.__effect.setOpacity(1)
		self.__animate.setDuration(300)
		self.__animate.finished.connect(self.__AnimateFinish)
		self.Set_Content(content)
		self.setGraphicsEffect(self.__effect)
	def Set_Content(self,wid):
		vbox=self.layout()
		if(self.__wid):
			vbox.removeWidget(self.__wid)
		self.__wid=wid
		if(wid):
			vbox.addWidget(wid)
	def Get_Content(self):
		return self.__wid
	def Set_Duration(self,duration):
		self.__animate.setDuration(duration)
	def show(self):
		super().show()
		self.__animate.stop()
		self.__animate.setEndValue(1)
		self.__animate.start()
	def hide(self):
		if(self.__trans):
			self.setAttribute(Qt.WA_TransparentForMouseEvents,True)
		self.__animate.stop()
		self.__animate.setEndValue(0)
		self.__animate.start()
	def __AnimateFinish(self):
		if(self.__effect.opacity()==0):
			super().hide() 
		else:
			self.setAttribute(Qt.WA_TransparentForMouseEvents,False)



