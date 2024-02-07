
__version__='1.0.0'
__author__='Ls_Jan'

import sys
import numpy as np
import cv2
from PyQt5.QtCore import Qt,QPoint,QRect,pyqtSignal
from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtGui import QPainter,QBitmap,QImage,QPixmap

__all__=['XJQ_Mask']
class XJQ_Mask(QLabel):
	'''
		1.即用即弃：蒙版对象创建时即刻生效，不用时通过mask.setParent(None)弃用即可，虽然可以调用mask.hide()暂时隐藏但意义不大
		2.可指定不遮挡的对象
		3.可指定特殊颜色，甚至是渐变色(因为本质是调用setStyleSheet函数进行设置的)
		4.可设置点击穿透以满足特殊场合
		5.遮罩单击时会触发``clicked``信号，用于实现“点击空白位置以取消”的操作
	'''
	__exclude=None
	clicked=pyqtSignal()
	def __init__(self,parent=None,*exclude,color='rgba(0,0,0,128)',clickBlock=True):
		super().__init__(parent)
		exclude=list(exclude)
		for pst in range(len(exclude)):
			if(type(exclude[pst])!=tuple):
				exclude[pst]=(exclude[pst],self.Trans_WidMask_Default)
			else:
				if(len(exclude[pst])<2):
					exclude[pst]=(exclude[pst][0],self.Trans_WidMask_Default)
				elif(type(exclude[pst][1])==bool):
					if(exclude[pst][1]==False):
						exclude[pst]=(exclude[pst][0],self.Trans_WidMask_Default)
					else:
						exclude[pst]=(exclude[pst][0],self.Trans_WidMask_Style)
		self.__exclude=exclude
		self.setAttribute(Qt.WA_TransparentForMouseEvents, not clickBlock)#鼠标事件穿透
		self.setStyleSheet(f'background:{color}')
		self.show()
	def mousePressEvent(self,event):
		self.clicked.emit()
	def paintEvent(self,event):
		if(not self.parent()):
			return
		self.resize(self.parent().size())

		bit=QBitmap(self.size())
		bit.fill(Qt.black)
		painter_bit=QPainter(bit)
		for item,offset in self.__Get_Offset().items():
			wid,trans=item
			pix=trans(wid)
			painter_bit.drawPixmap(QRect(offset,wid.size()),pix)
		painter_bit.end()

		super().paintEvent(event)
		self.setMask(bit)
	def __Get_Offset(self):
		record={}
		parent_self=self.parent()
		for item in self.__exclude:
			if(not item[0].isVisible()):
				continue
			wid=item[0]
			parent_wid=wid.parent()
			offset=QPoint(0,0)
			while (True):
				offset+=wid.pos()
				if(not parent_wid):
					break
				if(parent_wid==parent_self):
					break
				wid=wid.parent()
				parent_wid=wid.parent()
			if(parent_wid):
				record[item]=offset
		return record

	@classmethod
	def Trans_WidMask_Default(self,wid):
		pix=QPixmap(wid.size())
		pix.fill(Qt.white)
		return pix
	@classmethod
	def Trans_WidMask_Style(self,wid):
		arr=self.Trans_PixToArray(wid.grab())
		#洪填，将外围填充
		arr=cv2.cvtColor(arr,cv2.COLOR_RGBA2GRAY)
		h, w = arr.shape[:2]
		mask = np.zeros([h+2, w+2],np.uint8)
		arr_copy=arr.copy()
		arr=cv2.rectangle(arr,(0,0),(w-1,h-1),(int(arr[0][0]),))
		cv2.floodFill(arr, mask, (0,0), (0,), (2,), (2,), cv2.FLOODFILL_FIXED_RANGE)#参数是试出来的...懒得研究洪填
		arr=arr==arr_copy
		arr=arr*255
		arr=arr.astype(np.uint8)
		return self.Trans_ArrayToPix(arr)
	@staticmethod
	def Trans_PixToArray(pix):#pix是RGBA四通道QPixmap。不使用PIL.Image模块
		h,w=pix.height(),pix.width()
		buffer = QImage(pix).constBits()
		buffer.setsize(h*w*4)
		arr = np.frombuffer(buffer, dtype=np.uint8).reshape((h,w,4))
		return arr.copy()
	@staticmethod
	def Trans_ArrayToPix(arr):#arr对应四通道图片。不使用PIL.Image模块
		arr=cv2.cvtColor(arr,cv2.COLOR_RGBA2BGRA)
		img=QImage(arr.data, arr.shape[1], arr.shape[0], arr.shape[1]*4, QImage.Format_RGBA8888)
		return QPixmap(img)

