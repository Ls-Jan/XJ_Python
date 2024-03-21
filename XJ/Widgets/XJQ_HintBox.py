
__version__='1.0.0'
__author__='Ls_Jan'

from ..Functions.GetScreensArea import *
from ..Functions.CalcPopupArea import *

from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtCore import QEvent, QTimerEvent, Qt,QSize,QPoint,QRect,pyqtSignal
from PyQt5.QtGui import QCursor, QFocusEvent, QShowEvent

__all__=['XJQ_HintBox']
class XJQ_HintBox(QWidget):
	'''
		【特别补充】：
		该功能和QMenu有大幅重合，如果没有特殊需求的话建议优先使用QMenu，
		因为QMenu也是置顶显示，并且内容也可自定义，以及QMenu.popup函数可以使菜单窗口弹出在鼠标附近。

		置顶显示型容器，调用update函数可以使弹窗显示在鼠标附近，
		本质上是用来顶替只能显示纯文本的tooltip，
		弹窗与内容物的大小总是一致的。
		某种程度上甚至能用来替代QMenu(但没啥必要造轮子，QMenu提供的功能也足够使用的了

		可开启自动隐藏功能(在鼠标点击弹窗之外的地方弹窗会自动隐藏)，
		需注意的一点是该功能开启后弹窗显示时会将活跃窗口设置为本弹窗
	'''
	def __init__(self,content:QWidget=None,size:QSize=None):
		'''
			content为内容物。
			size为弹窗大小，为空则追随内容物大小。
		'''
		super().__init__()
		self.setAttribute(Qt.WA_TranslucentBackground, True)#透明背景。该属性要和Qt.FramelessWindowHint配合使用，单独用的话不生效
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.ToolTip)#无边框置顶窗体
		self.installEventFilter(self)
		self.__content=None
		self.__size=size
		self.__margin=10
		self.__autoHide=False
		self.Set_Content(content)
	def Set_AutoHide(self,flag:bool):
		'''
			用于实现自动隐藏功能，在弹窗弹出后如果点击其他地方那么弹窗会自动消失，
			特别的，开启自动隐藏时会将窗口焦点转移至弹窗上
		'''
		isVisible=self.isVisible()
		self.hide()
		self.__autoHide=flag
		if(isVisible):
			self.show()
		if(flag):
			self.activateWindow()
	def Set_Margin(self,margin:int):
		'''
			设置弹窗与鼠标之间的距离
		'''
		self.__margin=margin
	def Set_Content(self,content:QWidget):
		'''
			设置内容物
		'''
		if(self.__content):
			self.__content.hide()
			self.__content.setParent(None)
		if(content):
			content.setParent(self)
			content.setGeometry(QRect(QPoint(0,0),content.size()))
			content.show()
		self.__content=content
		self.update()
	def Get_Content(self):
		'''
			获取内容物
		'''
		return self.__content
	def resize(self,size:QSize):
		'''
			设置固定大小，如果size为None则大小追随内容物
		'''
		if(size):
			super().resize(size)
		self.__size=size
		self.update()
	def update(self,pos:QPoint=None):
		'''
			更新状态。
			可以指定坐标pos(不指定则默认鼠标位置)
		'''
		content=self.__content
		if(content):
			if(not self.__size):
				super().resize(content.size())
			else:
				content.resize(self.size())
		if(pos==None):
			pos=QCursor().pos()#获取鼠标位置：https://blog.csdn.net/weixin_43862688/article/details/108180908
		area=GetScreensArea(includeCursor=True)
		size=self.size()
		rst=CalcPopupArea(pos,size,area,self.__margin,True)
		if(rst):#如果鼠标在屏幕之外就可能会导致rst为空，以防万一
			self.setGeometry(rst[2])
			self.show()
		else:
			self.hide()
		super().update()
	def eventFilter(self,obj,event):
		if(event.type()==QEvent.WindowDeactivate):#窗口非活跃
			if(self.__autoHide):
				self.hide()
		return super().eventFilter(obj,event)
	def showEvent(self,event):
		if(self.__autoHide and self.__content):
			self.activateWindow()
		return super().showEvent(event)
