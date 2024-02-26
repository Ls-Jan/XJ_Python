
__version__='1.0.0'
__author__='Ls_Jan'

from ..Functions.GetQItemViewShowingIndices import *

from time import time
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtCore import QObject,QTimer

__all__=['XJQ_LazyLoadingPlugin']

class XJQ_LazyLoadingPlugin(QObject):
	'''
		用于实现Qt列表、表格控件的“懒加载”以及“过时资源自动释放”功能。
	'''
	__view=None
	__lst=None#长度与__view一致，记录时间以便确认哪些资源出现超时
	__index_curr=None#当前index
	__index_change=None#发生修改的index集合
	__timer_update=None#用于实现延时行为
	__timer_roll=None#用于实现超时释放
	__change=lambda indices,show:None#发生变化时该函数将被调用。indices是可遍历对象，对应的是索引值
	__rowExtend=None#额外加载范围值
	__retentionTime=None#资源留存时间(s)，超过该值时资源将被释放
	def __init__(self,view:QAbstractItemView):
		super().__init__(view)
		view.verticalScrollBar().valueChanged.connect(self.Opt_Update)
		timer_roll=QTimer()
		timer_roll.timeout.connect(self.__Func_Roll)
		timer_update=QTimer()
		timer_update.setSingleShot(True)
		timer_update.timeout.connect(self.__Func_Update)

		self.__index_curr=(-1,-1)
		self.__index_change=set()
		self.__view=view
		self.__rowExtend=0
		self.__lst=[]
		self.__timer_roll=timer_roll
		self.__timer_update=timer_update
		self.Set_DelayTime()
		self.Set_RollTime()
		self.Set_RetentionTime()
		self.Set_RowExtend()
		self.Opt_ListChange(0,view.model().rowCount(),insert=True)
		self.Opt_Update()
	def Set_RetentionTime(self,second:int=60):
		'''
			设置不被显示的行的资源留存时间(s)，当超过该时间时将会调用函数释放指定的行内容。
		'''
		self.__retentionTime=second
	def Set_DelayTime(self,second:int=0.5):
		'''
			设置停滞时间(s)，当调用Opt_Update后超过该时间时才会调用函数加载指定的行内容。
		'''
		timer=self.__timer_update
		isActive=timer.isActive()
		timer.stop()
		timer.setInterval(second*1000)
		if(isActive):
			timer.start()
	def Set_RollTime(self,second:int=10):
		'''
			设置轮转的时间间隔(s)，每隔一段时间便检测资源是否过时。
			一般不需要进行修改
		'''
		timer=self.__timer_roll
		isActive=timer.isActive()
		timer.stop()
		timer.setInterval(second*1000)
		if(isActive):
			timer.start()
	def Set_RowExtend(self,extend:int=5):
		'''
			用于预加载在显示区之外的行。
		'''
		self.__rowExtend=extend
	def Set_ChangeFunc(self,func):
		'''
			设置索引修改时调用的函数。
			func接受的参数为(indices,show:bool)，第一个参数为发生变化的行(只需关心它是可遍历对象)，第二个参数说明该是显示还是隐藏
		'''
		self.__change=func
	def Opt_Update(self):
		'''
			更新当前状态。该函数已经和目标控件的竖滚动条进行了绑定，该函数不再需要手动调用
		'''
		self.__timer_update.stop()
		self.__timer_update.start()
	def Opt_ListChange(self,start,count,*,remove=False,insert=False):
		'''
			当列表发生增删操作时，需要手动调用该函数以保证数据的同步
		'''
		lst=self.__lst
		if(remove):#移除
			del lst[start:start+count]
		else:#新增
			temp=lst[start:]
			del lst[start:]
			lst.extend([0]*count)
			lst.extend(temp)
	def __Func_Roll(self):
		lst=self.__lst
		change=self.__index_change
		remove=set()
		cTime=time()
		for i in change:
			if(cTime-lst[i]>self.__retentionTime):
				remove.add(i)
		change.difference_update(remove)
		if(remove):
			self.__change(remove,False)
		if(len(change)==0):#变动集空了那就关掉计时器
			self.__timer_roll.stop()
	def __Func_Update(self):
		oldIndex=self.__index_curr
		newIndex=GetQItemViewShowingIndices(self.__view,self.__rowExtend)
		self.__index_curr=newIndex
		newIndex=set(range(newIndex[0],newIndex[1]+1))
		oldIndex=set(range(oldIndex[0],oldIndex[1]+1)) if oldIndex[1]>=0 else newIndex
		self.__index_change.update(oldIndex-newIndex)#隐藏
		show=newIndex-self.__index_change#显示
		if(show):
			self.__change(show,True)
		cTime=time()
		for i in oldIndex.union(newIndex):
			self.__lst[i]=cTime
		if(not self.__timer_roll.isActive()):#开启计时器
			self.__timer_roll.start()
