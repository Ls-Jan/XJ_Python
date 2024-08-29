__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_SelectedPreviewMask']

from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter,QColor,QCursor

class XJQ_SelectedPreviewMask(QWidget):
	'''
		用于控件的选择可视化，主用于布局状态下的控件选择。
		原则上说，QListWidget之类的容器控件也能使用，但会出现一些小问题，而且话说回来这些容器控件都自带了选中高亮就没必要用这个遮罩控件。

		被依附的主控件在重写mousePressEvent时要去主动调用本类的Opt_Click函数。
	'''
	def __init__(self,parent:QWidget):
		super().__init__(parent)
		self.__wids=set()
		self.__col_selected=QColor(255,0,0,128)
		self.__lastWid=None
		self.__lastWidRemove=False
		self.__hold=False
		self.__valid=False
		self.setAttribute(Qt.WA_TransparentForMouseEvents, True)#鼠标事件穿透
		self.raise_()
	def Set_Color(self,selected:QColor):
		'''
			设置选中颜色
		'''
		self.__col_selected=selected
	def Set_SelectedWids(self,wids,exclude:bool=False):
		'''
			设置选中的控件。
			exclude为真则移除在wids中的控件。
		'''
		self.__wids=self.__wids.difference(wids) if(exclude) else set(wids)
		self.__valid=False
		self.update()
	def Get_SelectedWidgets(self):
		'''
			返回被选中的控件
		'''
		return self.__wids.copy()
	def Get_LastPressedWidget(self):
		'''
			返回最近一次被点击的控件，它同时是Opt_Press的返回结果。
		'''
		return self.__lastWid
	def Get_IsPressed(self):
		'''
			判断鼠标是否处于按下状态，
			在调用Opt_Press并且没调用Opt_Release、Opt_Clear、Set_SelectedWids时会返回真
		'''
		return self.__valid
	def Opt_Press(self,hold:bool=False):
		'''
			鼠标按下，会返回被选中的控件(可为空)。
			如果hold为真则为多选状态，并且点中已选中控件时不会立马状态反选，而是延后到Opt_Release的调用，该设计能很好的处理拖拽问题，
			即点击了AB两控件，然后Ctrl左击A控件时仍是AB选中状态，但调用Opt_Release后A会取消选中。
		'''
		wid=QApplication.widgetAt(QCursor.pos())
		if(wid==self.parent()):
			wid=None
		exist=wid in self.__wids
		if(not hold and not exist):
			self.__wids.clear()
		if(wid):
			self.__wids.add(wid)
			self.update()
		self.__hold=hold
		self.__lastWid=wid
		self.__lastWidRemove=exist
		self.__valid=True
		return wid
	def Opt_Drag(self):
		'''
			鼠标发生拖拽时调用该函数
		'''
		self.__hold=True
		self.__lastWidRemove=False
	def Opt_Release(self):
		'''
			见Opt_Press的说明，在复数控件选中时决定是否反选最近一次点击的控件。
		'''
		if(not self.__valid):
			return
		self.__valid=False
		if(not self.__hold):
			self.__wids.clear()
			self.__hold=True
			self.__lastWidRemove=False
		if(self.__lastWid):
			if(self.__lastWidRemove):
				if(self.__lastWid in self.__wids):
					self.__wids.remove(self.__lastWid)
			else:
				self.__wids.add(self.__lastWid)
			self.__lastWidRemove=False
		self.update()
	def Opt_Clear(self):
		'''
			重置状态
		'''
		self.Set_SelectedWids([])
		self.__lastWid=None
	def paintEvent(self,event):
		parent=self.parent()
		if(parent and parent.size()!=self.size()):
			self.resize(parent.size())
			return
		ptr=QPainter(self)
		for wid in self.__wids:
			if(wid.isVisible()):
				rect=wid.geometry()
				rect.setTopLeft(self.mapFromGlobal(wid.parent().mapToGlobal(rect.topLeft())))
				ptr.fillRect(rect,self.__col_selected)



