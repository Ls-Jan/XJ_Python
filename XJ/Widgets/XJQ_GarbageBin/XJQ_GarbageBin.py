__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_GarbageBin']
#TODO：2024/8/18
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class XJQ_GarbageBin(QLabel):
	'''
		一个垃圾桶控件，
		作用就是鼠标拖拽到本控件上释放时会触发deleted信号。
		图标自己设置，这里不负责。
	'''
	deleted=pyqtSignal(QMimeData)
	def __init__(self):
		super().__init__()
		self.__mData=QMimeData()
		self.setAcceptDrops(True)
	def __del__(self):
		del self.__mData
	def dragEnterEvent(self,event):
		cb=QApplication.clipboard()
		mDataSrc=event.mimeData()
		# mDataSrc=cb.mimeData()
		mData=self.__mData
		mData.clear()
		for fmt in mDataSrc.formats():
			print(fmt)
			print(mDataSrc.data(fmt))
			print()

		for fmt in mDataSrc.formats():#无脑全复制
			mData.setData(fmt,mDataSrc.data(fmt))
		# mDataSrc.setText("???")
		print("...")
		event.setDropAction(Qt.MoveAction)
		event.acceptProposedAction()
	def dropEvent(self,event):
		self.deleted.emit(self.__mData)
		mData=self.__mData
		# for fmt in mData.formats():
		# 	print(fmt)
		# 	print(mData.data(fmt))
		# 	print()


if True:
	app=QApplication([])
	gb=XJQ_GarbageBin()



	gb.show()
	gb.resize(640,480)
	app.exec()


