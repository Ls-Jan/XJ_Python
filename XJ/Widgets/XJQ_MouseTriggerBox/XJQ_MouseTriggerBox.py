
__version__='1.1.0'
__author__='Ls_Jan'
from typing import Union

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal,QEvent,QPoint,QRect,QRectF,Qt

__all__=['XJQ_MouseTriggerBox']
class XJQ_MouseTriggerBox(QWidget):
	'''
		鼠标触发器容器，自身不带布局。
		1.当鼠标进入指定区域时发出信号enter(str,QPoint,bool)并且第三参数为True，
			离开时触发enter信号并且第三参数为False，
		2.鼠标在指定区域停留一定时长时将发出信号hover(str,QPoint,bool)并且第三参数为True，
			触发hover信号后移动鼠标时将再次触发hover并且第三参数为False
		3.当设置父控件后该触发器总会自动调整位置大小使其完全恰好覆盖父控件(牛皮癣效果)(功能可禁用)(在调用setParent时第二参数autoResize决定是否启用功能)。
	'''
	enter=pyqtSignal(str,bool)
	hover=pyqtSignal(str,bool)
	def __init__(self,parent:QWidget=None,autoResize:bool=False):
		super().__init__()
		self.__area={}
		self.__cache={}
		self.__hover=set()
		self.__enter=set()
		self.__autoResize=False
		self.installEventFilter(self)
		self.setAttribute(Qt.WA_Hover,True)
		self.setParent(parent,autoResize)
		self.lower()
	def eventFilter(self,obj,event):
		eType=event.type()
		if(eType==QEvent.HoverMove):
			pos=event.pos()
			include=set()
			for name,area in self.__cache.items():
				if(area.contains(pos)):
					include.add(name)
			for name in include.difference(self.__enter):
				self.enter.emit(name,True)
			for name in self.__enter.difference(include):
				self.enter.emit(name,False)
			for name in self.__hover:
				self.hover.emit(name,False)
			self.__hover.clear()
			self.__enter=include
		elif(eType==QEvent.ToolTip):
			for name in self.__enter:
				self.hover.emit(name,True)
			self.__hover=self.__enter
		elif(eType==QEvent.Leave):
			for name in self.__enter:
				self.enter.emit(name,False)
			for name in self.__hover:
				self.hover.emit(name,False)
			self.__hover.clear()
			self.__enter.clear()
		elif(eType==QEvent.Resize or eType==QEvent.Move or eType==QEvent.Show):
			self.update()
		elif(eType==QEvent.Paint):
			parent=self.parent()
			if(parent and self.__autoResize):
				pSize=parent.size()
				if(self.size()!=pSize):
					self.resize(pSize)
		return False
	def setParent(self,parent:QWidget,autoResize:bool=False):
		'''
			设置父控件，如果autoResize为真那么触发器总会自动调整大小位置以恰好完全覆盖父控件
		'''
		super().setParent(parent)
		self.__autoResize=autoResize
		if(parent and autoResize):
			self.setGeometry(QRect(QPoint(0,0),parent.size()))
	def update(self,name:str=None):
		'''
			探测区位置发生变化时调用，窗体大小位置变化时会自动调用，一般不需要显式调用
		'''
		self.__cache.clear()
		keys=self.__area.keys()
		if(name in keys):
			keys=[name]
		for key in keys:
			area=self.__area[key]
			if(isinstance(area,QWidget)):
				rect=area.geometry()
				p1=area.mapToGlobal(QPoint(0,0))
				p2=self.mapFromGlobal(p1)
				rect.moveTo(p2)
				area=rect
			else:
				area=QRectF(area)
				attrs=['left','top','right','bottom']
				size=[self.width(),self.height()]
				for i in range(len(attrs)):
					attr=attrs[i]
					val=getattr(area,attr)()
					if(0<=val<=1):
						val=val*size[i%2]
						getattr(area,'set'+attr.capitalize())(val)#py字符串首字母大写：str.capitalize
				area=area.toRect()
			self.__cache[key]=area.normalized()
		super().update()
	def Get_Area(self,name:str):
		'''
			获取探测区，探测区不存在则返回None
		'''
		if(name not in self.__area):
			return None
		return self.__area[name]
	def Opt_AddArea(self,name:str,target:Union[QRectF,QWidget]):
		'''
			添加探测区，探测区可以是矩形也可以是控件。
			target如果是矩形，在坐标取值小于1时将视作百分比进行计算实际位置。
		'''
		if(isinstance(target,QWidget) or isinstance(target,QRectF)):
			self.__area[name]=target
			self.update(name)
			return True
		else:
			return False
	def Opt_RemoveArea(self,name:str):
		'''
			移除探测区
		'''
		if(name in self.__area):
			self.__area.pop(name)
			self.update()
			return True
		return False

