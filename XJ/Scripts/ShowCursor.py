'''
	点击查看不同光标，
	这里已经将光标所对应的含义写出来了
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

Qt.CursorShape.SizeAllCursor#十字
Qt.CursorShape.SizeFDiagCursor#左上右下
Qt.CursorShape.SizeBDiagCursor#左下右上
Qt.CursorShape.SizeHorCursor#水平
Qt.CursorShape.SizeVerCursor#竖直
Qt.CursorShape.ForbiddenCursor#禁用
Qt.CursorShape.PointingHandCursor#手指
Qt.CursorShape.CrossCursor#十字
Qt.CursorShape.ArrowCursor#箭头
Qt.CursorShape.BusyCursor#忙
Qt.CursorShape.WaitCursor#非常忙
Qt.CursorShape.BlankCursor#空白不显示

class CursorShow(QPushButton):
	def __init__(self):
		super().__init__()
		self.__keys=[key for key in dir(Qt) if key.find('Cursor')!=-1]
		self.__index=-1
		self.resize(500,200)
		self.__Next()
	def __Next(self):
		index=self.__index
		mod=len(self.__keys)
		while(True):
			try:
				index=(index+1)%mod
				key=self.__keys[index]
				self.setCursor(getattr(Qt,key))
				self.setText(key)
				if(index==0):
					print()
				print(key)
				break
			except:
				print('不存在：'+key)
		self.__index+=1
	def mousePressEvent(self,event):
		self.__Next()


if True:
	app = QApplication([])

	win=CursorShow()
	win.show()

	app.exec_()
