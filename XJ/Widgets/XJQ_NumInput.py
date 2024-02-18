
__version__='1.0.0'
__author__='Ls_Jan'

import re
from typing import Union
from PyQt5.QtCore import Qt,pyqtSignal
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

		特别的，精度是正数则是保留对应位的小数，负数则是舍弃对应位的整数，例如精度为-2那么数值取值会是0、100、200的形式(也就是调用round函数的效果)
	'''
	valueChanged=pyqtSignal(int)#槽信号，值修改时发送信号
	def __init__(self,
			  parent:QWidget=None,
			  valMin:Union[int,float]=None,
			  valMax:Union[int,float]=None,
			  precision:int=0,
			  step:Union[int,float]=None):
		'''
			valMin、valMax：指定最小最大值
			precision：设置数值精度
			step：作为滚轮的步进值使用
		'''
		super().__init__(parent)
		self.__min=None
		self.__max=None
		self.__curr=0
		self.__precision=precision
		self.__step=1
		self.setAlignment(Qt.AlignCenter)#设置对齐（默认居中
		self.setReadOnly(True)#设置只读，仅在双击时修改
		self.Set_ValueRange(valMin,valMax)
		self.Set_Precision(precision,step)
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
	def Set_Precision(self,precision:int=None,step:Union[int,float]=None):
		'''
			precision设置数值精度
			step作为滚轮的步进值使用
		'''
		if(precision!=None):
			self.__precision=precision
		mstep=pow(10,-self.__precision)
		if(step==None or step<mstep):
			step=mstep
		self.__step=step
		self.Set_Value(self.__curr)
	def Set_ValueRange(self,valMin:Union[int,float]=None,valMax:Union[int,float]=None):
		'''
			同时设置最小最大值
		'''
		if(valMin!=None and valMax!=None):
			if(valMax<valMin):
				valMin,valMax=valMax,valMin
		self.__val_min=valMin
		self.__val_max=valMax
		self.Set_Value(self.__curr)
	def Set_Value(self,val:Union[int,float]):
		'''
			设置当前值
		'''
		min=self.__val_min
		max=self.__val_max
		prec=self.__precision
		if(min!=None and val<min):
			val=min
		if(max!=None and val>max):
			val=max
		val=round(val,prec)
		val=float(val) if prec>0 else int(val)
		if(val!=self.__curr):
			self.__curr=val
			self.valueChanged.emit(val)
		super().setText(str(val))

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
		step=self.__step
		if(delta.y()<0):
			step=-step
		self.Set_Value(self.__curr+step)#滚轮向上滚动，增加
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
		





