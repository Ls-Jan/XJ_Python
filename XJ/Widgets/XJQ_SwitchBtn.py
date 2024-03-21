
__version__='1.0.0'
__author__='Ls_Jan'

from .XJQ_PureColorIconButton import XJQ_PureColorIconButton
from ..Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QAbstractButton,QStackedLayout,QSizePolicy
from PyQt5.QtCore import pyqtSignal

__all__=['XJQ_SwitchBtn']

class XJQ_SwitchBtn(QAbstractButton):#因为太过于常用，趁早把它组件化。
	'''
		开关按钮，状态发生变化时发送valueChanged(bool)信号，发送当前开关状态
	'''
	valueChanged=pyqtSignal(bool)#值修改时触发，发送当前开关状态
	__btns=None#依次是ON和OFF按钮
	__stk=None#0是ON按钮，1是OFF按钮
	def __init__(self,btnON:QAbstractButton=None,btnOFF:QAbstractButton=None):
		'''
			传入按钮，如果没指定那采用默认的纯色按钮
		'''
		super().__init__()
		if(btnON==None):
			btnON=XJQ_PureColorIconButton(GetRealPath('../Icons/播放.png'))
		if(btnOFF==None):
			btnOFF=XJQ_PureColorIconButton(GetRealPath('../Icons/暂停.png'))
		btnON.clicked.connect(lambda:self.Opt_Switch(True,isClicked=True))
		btnOFF.clicked.connect(lambda:self.Opt_Switch(False,isClicked=True))

		stk=QStackedLayout(self)
		stk.addWidget(btnON)
		stk.addWidget(btnOFF)
		self.__btns=[btnON,btnOFF]
		self.__stk=stk
		#debug半小时，找到核心，设置大小调整策略setSizePolicy：https://blog.csdn.net/qq_40732350/article/details/86703749
		#不调整的话按钮会最小的方式呈现(这好吗这不好)
		self.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
	def sizeHint(self):
		return self.__stk.currentWidget().sizeHint()
	def Get_IsON(self):
		'''
			获取当前开关状态
		'''
		return self.__stk.currentIndex()==1
	def Opt_Switch(self,ON=True,*,isClicked=False):
		'''
			切换当前状态，
			isClicked为真时如果发生切换那么还会发送clicked信号(主要给内部使用，外部调用不用管)
		'''
		i=1 if ON else 0
		if(self.__stk.currentIndex()!=i):
			self.__stk.setCurrentIndex(i)
			self.valueChanged.emit(ON)
			if(isClicked):
				self.clicked.emit()
	def Get_BtnON(self):
		'''
			获取按钮ON
		'''
		return self.__on
	def Get_BtnOFF(self):
		'''
			获取按钮OFF
		'''
		return self.__off
	def Set_BtnON(self,btn:QAbstractButton):
		'''
			设置按钮ON
		'''
		stk=self.__stk
		stk.takeAt(0)
		stk.insertWidget(0,btn)
		stk.setCurrentIndex(0)
		btn.clicked.connect(lambda:self.Opt_Switch(True))
		self.__btns[0].setParent(None)
		self.__btns[0]=btn
	def Set_BtnOFF(self,btn:QAbstractButton):
		'''
			设置按钮OFF
		'''
		stk=self.__stk
		stk.takeAt(1)
		stk.insertWidget(1,btn)
		stk.setCurrentIndex(1)
		btn.clicked.connect(lambda:self.Opt_Switch(False))
		self.__btns[1].setParent(None)
		self.__btns[1]=btn
	def paintEvent(self,event):#必须重写，哪怕是空的
		pass





