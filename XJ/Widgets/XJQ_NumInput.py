
__version__='1.0.0'
__author__='Ls_Jan'

import re
from PyQt5.QtCore import Qt,pyqtSignal,QTimer
from PyQt5.QtWidgets import QLineEdit,QWidget

__all__=['XJQ_NumInput']

class XJQ_NumInput(QLineEdit):
	'''
		数值输入框，用于简单的数值输入
		1、双击修改数值
		2、可滚轮调整
		3、可设置上下限
		4、可设置数值精度
		5、使用了正则匹配，有效防止数字以外的输入
		6、数值修改发出valueChanged信号(不建议连textChanged，在手动输入数值的过程中会频繁发出该信号，并不好用
		7、新增信号延迟发送功能，滚轮修改数值时不再频繁发送valueChanged信号

		特别的，精度取值是pow(10,n)，也就是形容100、1、0.1、0.01的数
	'''
	valueChanged=pyqtSignal(float)#槽信号，值修改时发送信号
	def __init__(self,
			  parent:QWidget=None,
			  valMin:float=0,
			  valMax:float=100,
			  val:float=None,
			  precision:float=1,
			  step:float=None):
		'''
			valMin、valMax：指定最小最大值
			precision：设置数值精度，取值是pow(10,n)
			step：作为滚轮的步进值使用
		'''
		super().__init__(parent)
		timer=QTimer()
		timer.setSingleShot(True)
		timer.setInterval(200)
		timer.timeout.connect(lambda:self.valueChanged.emit(self.__curr))
		val=val if val!=None else valMin
		self.__min=valMin
		self.__max=valMax
		self.__curr=val
		self.__precision=[0,0]#用于round函数的有效数字保留位
		self.__step=1
		self.__timer=timer
		self.setAlignment(Qt.AlignCenter)#设置对齐（默认居中
		self.setReadOnly(True)#设置只读，仅在双击时修改
		self.Set_ValueRange(valMin,valMax)
		self.Set_Precision(precision,step)
		self.Set_Value(val)
	def Set_Delay(self,delay:int):
		'''
			设置valueChanged信号的延迟触发功能，时间单位ms。
			该功能默认开启，时延200ms
		'''
		timer=self.__timer
		isActive=timer.isActive()
		timer.stop()
		timer.setInterval(delay)
		if(isActive):
			timer.start()
	def Get_Value(self):
		'''
			返回当前值
		'''
		return self.__curr
	def Get_ValueRange(self):
		'''
			返回取值范围
		'''
		return (self.__min,self.__max)
	def Set_Precision(self,precision:float=None,step:float=None):
		'''
			precision设置数值精度，取值是pow(10,n)
			step作为滚轮的步进值使用
		'''

		if(precision!=None and precision>0):
			self.__precision[0]=-self.__GetWeight(precision)
		mstep=pow(10,-self.__precision[0])
		if(step==None or step<mstep):
			step=mstep
		self.__step=step
		self.__precision[1]=-self.__GetWeight(step)
		self.Set_Value(self.__curr)
	def Set_ValueRange(self,valMin:float=None,valMax:float=None):
		'''
			同时设置最小最大值
		'''
		if(valMin!=None and valMax!=None):
			if(valMax<valMin):
				valMin,valMax=valMax,valMin
		self.__val_min=valMin
		self.__val_max=valMax
		self.Set_Value(self.__curr)
	def Set_Value(self,val:float):
		'''
			设置当前值
		'''
		min=self.__val_min
		max=self.__val_max
		prec=self.__precision[0]
		if(min!=None and val<min):
			val=min
		if(max!=None and val>max):
			val=max
		val=round(val,prec)
		val=float(val) if prec>0 else int(val)
		if(val!=self.__curr):
			self.__curr=val
			# self.valueChanged.emit(val)
			self.__timer.stop()
			self.__timer.start()
		super().setText(str(val))
	@staticmethod
	def __GetWeight(val):
		'''
			获取val的最大有效数字对应位权，
			例如0.074对应-2，444.9对应2
		'''
		sv=str(val)
		i=sv.find('.')
		if(val>=1):
			if(i>=0):
				sv=sv[:i]
			n=len(sv)-1
		elif(val>0):
			n=0
			sv=sv[i+1:]
			while(sv[n]=='0'):
				n+=1
			n=-1-n
		else:
			n=0
		return n
	
	def setText(self,tx=None):
		stx=self.text()
		if(tx==stx):
			return
		if(tx==None):
			tx=stx
		tx=re.search('[+\-]?\d*\.?\d*',tx).group()
		value=eval(tx) if tx else 0
		self.Set_Value(value)
	def setReadOnly(self,flag):
		super().setReadOnly(flag)
		self.setCursor(Qt.PointingHandCursor if flag else Qt.IBeamCursor)
		#QTextEdit好像不能直接self.setCursor来设置光标，得通过viewport才行
	def mouseDoubleClickEvent(self,event):
		self.setReadOnly(False)
	def wheelEvent(self,event):
		delta=event.angleDelta()
		step=self.__step if delta.y()>0 else -self.__step#滚轮向上滚动，增加
		val_1=round(self.__curr,self.__precision[1])
		val_2=val_1+step
		self.Set_Value(val_1 if self.__curr-val_2>1 else val_2)
	def keyPressEvent(self,event):
		if(event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter):#按下回车键
			self.setReadOnly(True)
			self.setText()
		else:
			super().keyPressEvent(event)            
	def focusOutEvent(self,event) -> None:
		self.setReadOnly(True)
		self.setText()
		return super().focusOutEvent(event)
		





