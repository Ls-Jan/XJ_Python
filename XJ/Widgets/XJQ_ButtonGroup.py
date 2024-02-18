
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtWidgets import QWidget,QRadioButton,QBoxLayout,QButtonGroup
from PyQt5.QtCore import Qt,pyqtSignal

__all__=['XJQ_ButtonGroup']
class XJQ_ButtonGroup(QWidget):
	'''
		按钮组，简单的封装，简单，同时能设置布局方向
		因为出现了“QRadioButton”在选中后无法取消的问题，特此封装，
		但只针对这个按钮哪够，除了QRadioButton外，也可以指定QCheckBox复选框按钮

		当鼠标点击按钮时发送信号stateChanged(str)
	'''
	stateChanged=pyqtSignal(str)
	def __init__(self,*,
			  btnType:type=QRadioButton,
			  clearClick:bool=True):
		'''
			btnType为按钮类型，默认QRadioButton(单选按钮)，也可以是QCheckBox(复选按钮)
			clearClick为真则可以让按钮清除选中状态
		'''
		super().__init__()
		self.__btnType=btnType
		self.__layout=QBoxLayout(QBoxLayout.TopToBottom,self)
		self.__group=QButtonGroup()
		self.__currBtn=None
		self.__group.buttonClicked.connect(self.__ClickButton)
		self.__btnLst=[]
		self.__clearClick=clearClick
		self.__group.setExclusive(btnType==QRadioButton)
	def Set_Direction(self,direction:QBoxLayout.Direction=QBoxLayout.TopToBottom):
		'''
			设置布局方向，QBoxLayout有四个方向可用，水平竖直各两个
		'''
		self.__layout.setDirection(direction)
	def Opt_AddButton(self,text:str):
		'''
			添加新的按钮
		'''
		btn=self.__btnType(text)
		self.__group.addButton(btn)
		self.__layout.addWidget(btn)
		self.__btnLst.append(btn)
		return True
	def Opt_ClearChecked(self):
		'''
			清除所有选中状态
		'''
		if(len(self.__btnLst)):
			btn=self.__btnLst[0]
			exclusive=self.__group.exclusive()
			self.__group.setExclusive(True)
			btn.setChecked(Qt.Checked)
			self.__group.setExclusive(False)
			btn.setChecked(Qt.Unchecked)
			self.__group.setExclusive(exclusive)
			self.__currBtn=None
		return True
	def Opt_ButtonRename(self,newText,*,index:int=None,text:str=None):
		'''
			按钮文本重命名，指定index或者text之一来确定是哪个按钮
		'''
		btn=self.__FindButton(index,text)
		if(btn):
			btn.setText(newText)
			return True
		return False
	def Opt_RemoveButton(self,*,index:int=None,text:str=None):
		'''
			按钮移除，指定index或者text之一来确定是哪个按钮
		'''
		btn=self.__FindButton(index,text)
		if(btn):
			self.__btnLst.remove(btn)
			self.__group.removeButton(btn)
			return True
		return False
	def Get_CheckedLst(self):
		'''
			获取被选中的按钮组(列表)
		'''
		lst=[]
		for btn in self.__btnLst:
			if(btn.isChecked()):
				lst.append(btn.text())
		return lst
	def Set_Checked(self,checked:bool,*,index:int=None,text:str=None):
		'''
			设置指定按钮的选中状态
		'''
		btn=self.__FindButton(index,text)
		if(btn):
			btn.setChecked(checked)
			return True
		return False
	def Set_Exclusive(self,flag:bool):
		'''
			设置单选模式
		'''
		self.__group.setExclusive(flag)
		if(not flag):
			self.__currBtn=None
		return True
	def __FindButton(self,index:int=None,text:str=None):
		if(index!=None):
			if(0<=index<len(self.__btnLst)):
				return self.__btnLst[index]
		elif(text!=None):
			for btn in self.__btnLst:
				if(btn.text()==text):
					return btn
		return None
	def __ClickButton(self,btn:QWidget):
		tx=btn.text()
		if(self.__group.exclusive()):
			if(self.__currBtn==btn):
				if(self.__clearClick):
					self.__group.setExclusive(False)
					btn.setChecked(Qt.Unchecked)
					self.__group.setExclusive(True)
					btn=None
					tx=''
				else:
					return
		self.stateChanged.emit(tx)
		self.__currBtn=btn
