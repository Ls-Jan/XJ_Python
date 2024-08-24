__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_GarbageBin']

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal,QMimeData,QSize,Qt
from XJ.Functions.GetRealPath import GetRealPath
from typing import Union
from ..XJQ_AutoSizeLabel import XJQ_AutoSizeLabel

# 拖拽事件的参考文章：https://blog.csdn.net/g310773517/article/details/140217677
class XJQ_GarbageBin(XJQ_AutoSizeLabel):
	'''
		一个垃圾桶控件，作用就是鼠标拖拽到本控件上释放时会触发deleted(QMimeData)信号。
		图标可以通过setPixmap进行替换。
	'''
	dropped=pyqtSignal(QMimeData)
	def __init__(self,icon:Union[QPixmap,str]=None,size:QSize=QSize(128,128),minSize:QSize=QSize(64,64)):
		'''
			接受一个垃圾桶图标，可传入文件路径或是QPixmap对象，如果传入空则使用默认图标。
			size为控件图标大小，minSize为控件最小大小。
		'''
		super().__init__()
		if(icon==None):
			icon=GetRealPath('./图标-垃圾桶.ico')
		if(isinstance(icon,str)):
			icon=QPixmap(icon)
		self.setPixmap(icon.scaled(size))
		self.setMinimumSize(minSize)
		self.__mData=QMimeData()#拖拽消息的数据拷贝
		self.setAcceptDrops(True)
	def __del__(self):
		del self.__mData
	def dragEnterEvent(self,event):
		mDataSrc=event.mimeData()
		mData=self.__mData
		mData.clear()
		for fmt in mDataSrc.formats():#无脑全复制
			mData.setData(fmt,mDataSrc.data(fmt))
		event.setDropAction(Qt.MoveAction)
		event.accept()#并不建议使用event.acceptProposedAction
	def dropEvent(self,event):
		self.dropped.emit(self.__mData)



	

