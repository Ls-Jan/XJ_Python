from PyQt5.QtWidgets import QWidget,QRadioButton,QHBoxLayout,QButtonGroup
from PyQt5.QtCore import Qt,pyqtSignal

__all__=['XJQ_ButtonGroup']
class XJQ_ButtonGroup(QWidget):
	'''
		按钮组，简单的封装，简单
		因为出现了“QRadioButton”在选中后无法取消的问题，特此封装，
		但只针对这个按钮哪够，除了QRadioButton外，也可以指定QCheckBox复选框按钮
	'''
	changed=pyqtSignal(str)
	def __init__(self,*,btnType=QRadioButton,layout=QHBoxLayout,clearClick=True):
		super().__init__()
		self.__btnType=btnType
		self.__layout=layout(self)
		self.__group=QButtonGroup()
		self.__currBtn=None
		self.__group.buttonClicked.connect(self.__ClickButton)
		self.__btnLst=[]
		self.__clearClick=clearClick
		self.__group.setExclusive(btnType==QRadioButton)
	def Opt_AddButton(self,text):
		btn=self.__btnType(text)
		self.__group.addButton(btn)
		self.layout().addWidget(btn)
		self.__btnLst.append(btn)
		return True
	def Opt_ClearChecked(self):#清除所有选中状态
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
	def Opt_ButtonRename(self,newText,*,index=None,text=None):
		btn=self.__FindButton(index,text)
		if(btn):
			btn.setText(newText)
			return True
		return False
	def Opt_RemoveButton(self,*,index=None,text=None):
		btn=self.__FindButton()
		if(btn):
			self.__btnLst.remove(btn)
			self.__group.removeButton(btn)
			return True
		return False
	def Get_CheckedLst(self):
		lst=[]
		for btn in self.__btnLst:
			if(btn.isChecked()):
				lst.append(btn.text())
		return lst
	def Set_Current(self,*,index=None,text=None):
		btn=self.__FindButton(index,text)
		if(btn):
			btn.setChecked(Qt.Checked)
			return True
		return False
	def Set_Exclusive(self,flag):
		self.__group.setExclusive(flag)
		if(not flag):
			self.__currBtn=None
		return True
	def __FindButton(self,index=None,text=None):
		if(index!=None):
			if(0<=index<len(self.__btnLst)):
				return self.__btnLst[index]
		elif(text!=None):
			for btn in self.__btnLst:
				if(btn.text()==text):
					return btn
		return None
	def __ClickButton(self,btn):
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
		self.changed.emit(tx)
		self.__currBtn=btn
