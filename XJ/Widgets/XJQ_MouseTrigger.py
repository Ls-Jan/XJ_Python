
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt,QObject,QRect,pyqtSignal,QEvent



__all__=['XJQ_MouseTrigger']

class XJQ_MouseTrigger(QObject):#当鼠标进出指定区域时发出信号
	'''
		当鼠标进出控件指定区域时发出信号
		创建对象时需指定目标控件。

		由于能力有限，暂未找到“向兄弟控件传递事件”的有效方法
		底层采用的是对目标控件安装事件过滤器的方法实现的鼠标追踪
		底层对目标控件调用了两个函数：setMouseTracking、installEventFilter
		也就是本类与目标控件出现了不可避免的耦合
	'''
	enter=pyqtSignal(str,bool)#为真则enter，为假则leave
	def __init__(self,win):
		super().__init__(win)
		win.setMouseTracking(True)#鼠标跟踪
		win.installEventFilter(self)
		self.__range=[]
		self.__cache=[]
		self.__active=set()
	def eventFilter(self,obj,event):
		eType=event.type()
		if(eType==QEvent.MouseMove):
			self.__UpdateActive(event.pos())
		elif(eType==QEvent.Enter):
			self.__UpdateActive(event.pos())
		elif(eType==QEvent.Leave):
			for name in self.__active:
				self.enter.emit(name,False)
			self.__active.clear()
		elif(eType==QEvent.Resize):
			self.__UpdateCache()
		return False
	def Opt_AddRange(self,name,pos=(0.0,0.0),size=(1.0,1.0),*,target=None):#添加探测区
		if(isinstance(target,QWidget)):
			self.__range.append((name,target))
		else:
			self.__range.append((name,(pos,size)))
		self.__UpdateCache()
	def Opt_RemoveRange(self,name):#移除探测区
		for i in range(len(self.__range)-1,-1,-1):
			if(self.__range[i][0]==name):
				self.__range.pop(i)
				self.__UpdateCache()
				return True
		return False
	def __UpdateCache(self):
		self.__cache.clear()
		win=self.parent()
		pSize=win.size()
		pSize=(pSize.width(),pSize.height())
		for item in self.__range:
			name,target=item
			if(isinstance(target,QWidget)):
				pos=target.pos()
				size=target.size()
				if(target.parent()!=win):
					pos=target.mapTo(win,pos)
				pos=[pos.x(),pos.y()]
				size=[size.width(),size.height()]
			else:
				pos=list(target[0])
				size=list(target[1])
			for i in range(2):
				if(isinstance(pos[i],float)):
					pos[i]=pSize[i]*pos[i]
				if(isinstance(size[i],float)):
					size[i]=pSize[i]*size[i]
			self.__cache.append((name,QRect(*pos,*size)))
	def __UpdateActive(self,pos):
		active=set()
		for item in self.__cache:
			name,rect=item
			if(rect.contains(pos)):
				active.add(name)
		for name in active.difference(self.__active):
			self.enter.emit(name,True)
		for name in self.__active.difference(active):
			self.enter.emit(name,False)
		self.__active=active
