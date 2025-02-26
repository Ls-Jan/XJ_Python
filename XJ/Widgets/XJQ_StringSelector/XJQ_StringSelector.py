__version__='1.0.1'
__author__='Ls_Jan'
__all__=['XJQ_StringSelector']

from PyQt5.QtWidgets import QLineEdit,QListView,QLabel,QStyle
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QPixmap
from PyQt5.QtCore import QObject,pyqtSignal,QModelIndex,Qt

from typing import List,Set
from .TextEditDelegate import TextEditDelegate

class XJQ_StringSelector(QObject):
	'''
		字串选择器，基于QListView，
		选择的途中可新增选项。
	'''
	createNewString=pyqtSignal(str)
	__lv:QListView
	__le:QLineEdit
	__disableSet:Set[str]
	__appendHint:str
	__disableMark:QLabel
	def __init__(self,lv:QListView=None):
		super().__init__()
		lv=lv if lv else QListView()
		model=QStandardItemModel()
		lv.setModel(model)
		self.__lv=lv
		self.__le=None
		self.__disableSet=set()
		self.__appendHint='<新增>'
		self.__disableMark=QLabel(lv)

		ted=TextEditDelegate()
		lv.setItemDelegate(ted)
		lv.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
		ted.newEditor.connect(self.__InitEditor)
		ted.closeEditor.connect(self.__CloseEditor)
		ted.alignCenter=True
		lb=self.__disableMark
		lb.setPixmap(lb.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning).pixmap(24,24))
		lb.setScaledContents(True)
		self.Set_SelectableList([])
	def Set_SelectableList(self,lst:List[str]):
		'''
			设置可选项
		'''
		model:QStandardItemModel=self.__lv.model()
		model.clear()
		lst.append('')
		for i in range(len(lst)):
			item=QStandardItem(lst[i])
			model.setItem(i,0,item)
			item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
			item.setEditable(False)
		self.__UpdateLastRow()
	def Get_ListView(self):
		'''
			返回列表控件
		'''
		return self.__lv
	def Set_AdditionHint(self,hint:str):
		'''
			设置末行“新增项”的文本内容
		'''
		self.__appendHint=hint
		self.__UpdateLastRow()
	def Opt_CancelLastString(self):
		'''
			可以通过该函数来撤回最近一次添加的字串(与信号createNewString组合使用)
		'''
		model:QStandardItemModel=self.__lv.model()
		count=model.rowCount()
		if(count>1):
			row=count-2
			self.__disableSet.discard(model.item(row,0).text())
			model.removeRow(row)
	def Set_DisableMark(self,pix:QPixmap):
		'''
			设置不可用时显示的标志(尽量正方形的小图标)
		'''
		self.__disableMark.setPixmap(pix)
		self.__UpdateLastRow()
	def Set_DisableList(self,lst:List[str]):
		'''
			设置不可用的内容
		'''
		self.__disableSet=set(lst)
		self.__UpdateLastRow()
	def __UpdateLastRow(self):
		'''
			更新末行的内容
		'''
		model:QStandardItemModel=self.__lv.model()
		mark=self.__disableMark
		if(self.__le):
			margin=2
			le=self.__le
			tx=le.text()
			if True:#手动居中编辑框
				w=le.width()
				W=le.parent().width()
				le.move((W-w)>>1,le.y())
			if(tx in self.__disableSet):
				sz=le.size()
				w,h=sz.width(),sz.height()-margin*2
				mark.setGeometry(w-h,margin,h,h)
				mark.show()
			else:
				mark.hide()
		else:
			item=model.item(model.rowCount()-1,0)
			item.setText(self.__appendHint)
			item.setEditable(True)
			mark.hide()
	def __InitEditor(self,le:QLineEdit,index:QModelIndex):
		'''
			对弹出的文本框进行编辑
		'''
		model:QStandardItemModel=self.__lv.model()
		model.itemFromIndex(index).setText('')
		le.textChanged.connect(self.__UpdateLastRow,Qt.ConnectionType.UniqueConnection)
		self.__disableMark.setParent(le)
		self.__le=le
		self.__UpdateLastRow()
	def __CloseEditor(self):
		'''
			关闭编辑器		
		'''
		tx=self.__le.text()
		if(tx and tx not in self.__disableSet):
			self.__disableSet.add(tx)
			model:QStandardItemModel=self.__lv.model()
			count=model.rowCount()
			item=model.item(count-1,0)
			item.setEditable(False)
			item=QStandardItem('')
			item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
			model.setItem(count,0,item)#追加新行
			self.createNewString.emit(tx)
		self.__le=None
		self.__disableMark.setParent(self.__lv)
		self.__UpdateLastRow()






