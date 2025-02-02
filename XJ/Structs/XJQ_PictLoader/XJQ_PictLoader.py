
__version__='1.0.0'
__author__='Ls_Jan'

from .XJQ_GettingPixmapTask import XJQ_GettingPixmapTask

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject,pyqtSignal,QThreadPool
from time import sleep

__all__=['XJQ_PictLoader']
class XJQ_PictLoader(QObject):
	'''
		用于本地视频/动图的图片异步加载，使用Qt线程池完成，返回结果是QPixmap。
		需依赖XJ_Frame提供图片元数据。

		每个图片读取完毕后会发出loaded(int,QPixmap)信号，第一个信号代表id值。
		当所有任务全都完成时发送finished信号。
	'''
	loaded=pyqtSignal(int,QPixmap)
	finished=pyqtSignal()
	def __init__(self,pool:QThreadPool=None)->None:
		'''
			如果没有指定池子那么就会自动创建一个线程池QThreadPool。
		'''
		super().__init__()
		if(pool==None):
			pool=QThreadPool(self)
			pool.setMaxThreadCount(1)
		self.__pool=pool
		self.__delayTime=0.01
		self.__tasks={}
		self.Set_DelayTime()
		QApplication.instance().aboutToQuit.connect(self.Opt_Clear)
	def Set_ThreadCount(self,count:int=1)->None:
		'''
			设置最大线程数，默认为1
		'''
		self.__pool.setMaxThreadCount(count)
	def Set_DelayTime(self,msec:int=10):
		'''
			为每个任务完成后的一小段延迟(ms)，以避免任务持续占用CPU资源
		'''
		self.__delayTime=msec/1000
	def Opt_Remove(self,*ids)->None:
		'''
			移除指定id所对应的任务
		'''
		tasks=self.__tasks
		for id in ids:
			if(id in tasks):
				task=tasks.pop(id)
				self.__pool.tryTake(task)
	def Opt_Append(self,*tasks)->None:
		'''
			添加图片读取任务，每个task的数据为(int,XJ_Frame,tuple,bool)，依次对应id值、XJ_Frame对象、要获取的图片大小、是否允许图片放大。
			如果未指定大小那么将采用图片原大小
		'''
		for data in tasks:
			task=XJQ_GettingPixmapTask(*data,callback=self.__Callback)
			self.Opt_Remove(data[0])
			self.__tasks[data[0]]=task
			self.__pool.start(task)
	def __Callback(self,id,pix)->None:
		'''
			单纯发送loaded信号和finished信号
		'''
		if(id in self.__tasks):
			self.loaded.emit(id,pix)
			self.__tasks.pop(id)
		if(len(self.__tasks)==0):
			self.finished.emit()
		sleep(self.__delayTime)
	def Opt_Clear(self)->None:
		'''
			清空池子。
			该操作已经与QApplication对象的AboutToQuit信号关联，在程序退出时会自动调用。
		'''
		self.__tasks.clear()
		self.__pool.clear()
		self.__pool.waitForDone()



