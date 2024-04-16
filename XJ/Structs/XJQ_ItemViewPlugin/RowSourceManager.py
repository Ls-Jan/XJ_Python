
__version__='1.0.0'
__author__='Ls_Jan'

from ...Functions.GetQItemViewShowingIndices import GetQItemViewShowingIndices

from time import time
from PyQt5.QtWidgets import QAbstractItemView,QApplication
from PyQt5.QtCore import QObject,QTimer,pyqtSignal

__all__=['RowSourceManager']

class RowSourceManager(QObject):
	'''
		用于实现Qt列表/表格控件的“懒加载”以及“过时资源自动释放”功能。
		会发送rowShowChanged(indices:list,show:bool)信号，
		indices为发生更新的行索引列表(已排序)，show说明这些行是显示还是隐藏。
		需要注意的是当列表的行发生变化时需及时调用Opt_ListChange同步内部数据。

		关键参数说明以及默认值如下：
		RetentionTime-资源留存时间(30s)：不被显示的行经过该时间后会发送rowShowChanged信号；
		DelayTime-延时加载(0.5s)：在列表/表格的竖滚动条不再移动超过一定时间后会发送rowShowChanged信号；
		RollTime-定时检查(10s)：用于定期检查资源是否过期(该操作没有性能影响)，值不宜过大，需比RetentionTime小(不然RetentionTime就没意义了)
		rowExtend-额外加载的行数(5)：少量加载显示区之外的行。
		rowCountMax-最大加载行数(1000)：当已加载的行数超过该值时会保留0.95*rowCountMax数量资源，其余最旧资源强制释放
	'''
	rowShowChanged=pyqtSignal(list,bool)
	__view=None
	__lst=None#长度与__view一致，记录时间以便确认哪些资源出现超时
	__index_curr=None#当前index
	__index_cache=None#发生修改的index集合
	__timer_update=None#用于实现延时行为
	__timer_roll=None#用于实现超时释放
	__rowExtend=None#额外加载范围值
	__retentionTime=None#资源留存时间(s)，超过该值时资源将被释放
	__rowCountMax=None#行加载最大数量
	def __init__(self,view:QAbstractItemView):
		super().__init__(view)
		view.verticalScrollBar().valueChanged.connect(self.Opt_Update)
		timer_roll=QTimer()
		timer_roll.timeout.connect(self.__Func_Roll)
		timer_update=QTimer()
		timer_update.setSingleShot(True)
		timer_update.timeout.connect(self.__Func_Update)

		self.__index_curr=(-1,-1)
		self.__index_cache=set()
		self.__view=view
		self.__rowExtend=0
		self.__lst=[]
		self.__timer_roll=timer_roll
		self.__timer_update=timer_update
		self.Set_DelayTime()
		self.Set_RollTime()
		self.Set_RetentionTime()
		self.Set_RowExtend()
		self.Set_RowCountMax()
		self.Opt_Update()
		if(view.model()):
			self.Opt_ListChange(0,view.model().rowCount(),insert=True)
		QApplication.instance().aboutToQuit.connect(self.Opt_Stop)
	def Get_ShowingRow(self,extend=None):
		'''
			获取当前显示着的行，返回的是列表。
			extend为None则使用设置好的rowExtend值
		'''
		if(extend==None):
			extend=self.__rowExtend
		index=GetQItemViewShowingIndices(self.__view,extend)
		return list(range(index[0],index[1]+1))
	def Set_RetentionTime(self,second:int=30):
		'''
			设置不被显示的行的资源留存时间(s)，当超过该时间时将会调用函数释放指定的行内容。
		'''
		self.__retentionTime=second
	def Set_DelayTime(self,second:int=0.5):
		'''
			设置停滞时间(s)，当调用Opt_Update后超过该时间时才会调用函数加载指定的行内容。
		'''
		self.__timer_update.setInterval(second*1000)
	def Set_RollTime(self,second:int=10):
		'''
			设置轮转的时间间隔(s)，每隔一段时间便检测资源是否过时。
			一般不需要进行修改
		'''
		self.__timer_roll.setInterval(second*1000)
	def Set_RowExtend(self,extend:int=5):
		'''
			用于调整在显示区之外预加载的行数。
		'''
		self.__rowExtend=extend
	def Set_RowCountMax(self,count:int=1000):
		'''
			设置行加载最大数量。
			当已加载的行数超过该值时会保留0.95*rowCountMax数量资源，其余最旧资源强制释放
		'''
		self.__rowCountMax=count
	def Opt_Update(self):
		'''
			更新当前状态。该函数已经和目标控件的竖滚动条进行了绑定，该函数不再需要手动调用
		'''
		self.__timer_update.stop()
		self.__timer_update.start()
	def Opt_Stop(self):
		'''
			停止刷新。
			该操作已经与QApplication对象的AboutToQuit信号关联，在程序退出时会自动调用。
		'''
		self.__timer_update.stop()
		self.__timer_roll.stop()
	def Opt_ListChange(self,start,count,*,remove=False,insert=False):
		'''
			当列表发生增删操作时，需要手动调用该函数以保证数据的同步
		'''
		self.__timer_roll.stop()
		self.__timer_update.stop()
		oldIndex=self.__index_curr
		if(oldIndex[1]>=0):
			oldIndex=set(range(oldIndex[0],oldIndex[1]+1))
			cTime=time()
			for i in oldIndex:
				self.__lst[i]=cTime
		self.__index_curr=[-1,-1]
		lst=self.__lst
		cache_before=self.__index_cache
		cache_after=set()
		if(remove):#移除
			stop=start+count
			del lst[start:stop]
			for i in cache_before:
				if(i>=start):
					if(i<stop):
						continue
					i-=count
				cache_after.add(i)
		elif(insert):#新增
			temp=lst[start:]
			del lst[start:]
			lst.extend([0]*count)
			lst.extend(temp)
			for i in cache_before:
				if(i>=start):
					i+=count
				cache_after.add(i)
		self.__index_cache=cache_after
		self.__timer_update.start()
	def __Func_Roll(self):
		lst=self.__lst
		cache=self.__index_cache
		remove=set()
		cTime=time()
		for i in cache:
			if(cTime-lst[i]>self.__retentionTime):
				remove.add(i)
		cache.difference_update(remove)
		if(remove):
			self.rowShowChanged.emit(sorted(remove),False)
		if(len(cache)==0):#变动集空了那就关掉计时器
			self.__timer_roll.stop()
	def __Func_Update(self):
		oldIndex=self.__index_curr
		newIndex=GetQItemViewShowingIndices(self.__view,self.__rowExtend)
		self.__index_curr=newIndex
		newIndex=set(range(newIndex[0],newIndex[1]+1))
		oldIndex=set(range(oldIndex[0],oldIndex[1]+1)) if oldIndex[1]>=0 else newIndex
		self.__index_cache.update(oldIndex-newIndex)#隐藏
		show=newIndex-self.__index_cache#显示
		cTime=time()
		for i in oldIndex.union(newIndex):#因为直到newIndex显示之前的那一刻一直显示着oldIndex，当然也要把oldIndex的时间更新一遍
			self.__lst[i]=cTime
		if(len(self.__index_cache)>self.__rowCountMax):
			lst=[(self.__lst[i],i) for i in self.__index_cache]
			lst.sort(reverse=True)
			remove=[item[1] for item in lst[int(self.__rowCountMax*0.95):]]
			self.rowShowChanged.emit(sorted(remove),False)
		if(len(show)>0):
			self.rowShowChanged.emit(sorted(show),True)
		if(not self.__timer_roll.isActive()):#开启计时器
			self.__timer_roll.start()
