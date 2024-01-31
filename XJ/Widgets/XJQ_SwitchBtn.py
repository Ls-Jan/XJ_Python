
from PyQt5.QtWidgets import QWidget,QStackedLayout
from PyQt5.QtCore import pyqtSignal

from .XJQ_IconButton import *
from ..Functions import GetRealPath

__all__=['XJQ_SwitchBtn']

class XJQ_SwitchBtn(QWidget):#因为太过于常用，趁早把它组件化。
	'''
		开关按钮
	'''
	valueChanged=pyqtSignal(bool)#值修改时触发，发送当前开关状态
	__off=None
	__on=None
	__stk=None#0是ON按钮，1是OFF按钮
	def __init__(self,iconOn=None,iconOff=None):
		super().__init__()
		if(iconOn==None):
			iconOn=GetRealPath('./icons/播放.png')
		if(iconOff==None):
			iconOff=GetRealPath('./icons/暂停.png')
		on=XJQ_IconButton(iconOn)
		off=XJQ_IconButton(iconOff)
		stk=QStackedLayout(self)

		on.clicked.connect(lambda:self.Opt_Switch(True))
		off.clicked.connect(lambda:self.Opt_Switch(False))
		stk.addWidget(on)
		stk.addWidget(off)
		self.__on=on
		self.__off=off
		self.__stk=stk
	def Get_IsON(self):
		return self.__stk.currentIndex()==1
	def Opt_Switch(self,ON=True):
		self.__stk.setCurrentIndex(1 if ON else 0)
		self.valueChanged.emit(ON)
	def Get_BtnON(self):
		return self.__on
	def Get_BtnOFF(self):
		return self.__off
	def Set_BtnON(self,btn):
		stk.takeAt(0)
		stk.insertWidget(0,btn)
		stk.setCurrentIndex(0)
		btn.clicked.connect(lambda:self.Opt_Switch(True))
		self.__on.setParent(None)
		self.__on=btn
	def Set_BtnOFF(self,btn):
		stk.takeAt(1)
		stk.insertWidget(1,btn)
		stk.setCurrentIndex(1)
		btn.clicked.connect(lambda:self.Opt_Switch(False))
		self.__off=btn
		self.__off.setParent(None)




