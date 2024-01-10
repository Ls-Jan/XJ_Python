


from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon,QPixmap,QImage,QPalette
from PyQt5.QtWidgets import QStyleOption,QStyleOptionButton

import cv2
import numpy as np
from functools import reduce

__all__=['XJQ_Icon']
class XJQ_Icon(QIcon):#纯色图标
	'''
		纯色图标，可改图标色以及背景色，以及可以预置/修改图标大小(调用pixmap函数时可不必再传入大小参数了)。
		当然，类似QPushButton在调用setIcon后，icon发生更新时QPushButton显示的图标并不会发生改变，需要再次调用setIcon才行
	'''
	def __init__(self,data,fg=(0,255,0,255),bg=(0,0,0,0),size=(20,20),hint=None):#data可以为图片路径(str)或是图片数据(np.ndarray)
		# QIcon：https://doc.qt.io/qt-6/qicon.html
		super().__init__()
		if(isinstance(data,np.ndarray)):
			im=data
		elif(isinstance(data,str)):
			im=self.Opt_LoadPictAsArray(data)
		else:
			raise Exception('data参数错误，类型仅能为np.ndarray(图片数据)或是str(图片路径)')
		if(len(fg)==3):
			fg=(*fg,255)
		if(len(bg)==3):
			bg=(*bg,255)

		msk=cv2.split(im)[3]
		# msk=reduce(lambda a,b:a|b,cv2.split(im))#废弃，更多时候只需要关注alpha的值
		self.__msk=cv2.threshold(msk,127,255,cv2.THRESH_BINARY)[1]
		#cv2纯色图：https://blog.csdn.net/qq_45666248/article/details/107666586
		self.__bg=np.zeros((*msk.shape,4),np.uint8)
		self.__fg=np.zeros((*msk.shape,4),np.uint8)
		self.__bg[:] = bg
		self.__fg[:] = fg
		self.__size=QSize(*size)
		self.__hint=hint
		self.__UpdatePixmap()
	def Set_ForeColor(self,fg):
		if(len(fg)==3):
			fg=(*fg,255)
		self.__fg[:] = fg
		self.__UpdatePixmap()
	def Set_BackColor(self,bg):
		if(len(bg)==3):
			bg=(*bg,255)
		self.__bg[:] = bg
		self.__UpdatePixmap()
	def Set_FBColorFromWid(self,wid):#根据wid来决定前景背景色(不靠谱，时灵时不灵)
		#获取控件颜色(本质获取调色板)：https://blog.csdn.net/c_shell_python/article/details/98895712
		pt=wid.palette()
		fg=pt.text().color()
		# bg=pt.button().color()
		bg=pt.base().color()
		cols=list(map(lambda col:[getattr(col,ch)() for ch in ['red','green','blue','alpha']],[fg,bg]))
		self.__fg[:] = cols[0]
		self.__bg[:] = cols[1]
		self.__UpdatePixmap()
	def pixmap(self,*arg):#少写额外的大小参数，很好
		if(arg):
			return super().pixmap(*arg)
		return super().pixmap(self.__size)
	def size(self):#特殊场合有用
		return self.__size
	def hint(self):#特殊场合有用
		return self.__hint
	def __UpdatePixmap(self):
		#模运算bitwise_and：https://blog.csdn.net/qq_40210586/article/details/106572504
		fg=self.__fg
		bg=self.__bg
		fg=cv2.bitwise_and(fg,fg, mask=self.__msk)
		bg=cv2.addWeighted(bg,1,fg,1,0)
		pix=self.Trans_ArrayToPixmap(bg)
		#虽然没有setPixmap但有这个addPixmap函数，简单看了下这个函数的功能，符合预期，很好
		#https://wenku.baidu.com/view/8d3284563269a45177232f60ddccda38376be1ba.html
		self.addPixmap(pix)
	@staticmethod
	def Opt_LoadPictAsArray(path):
		#cv2读取中文路径图片：https://www.zhihu.com/question/67157462/answer/251754530
		return cv2.imdecode(np.fromfile(path,dtype=np.uint8),cv2.IMREAD_UNCHANGED)
	@staticmethod
	def Trans_ArrayToPixmap(arr):#arr对应四通道图片。不使用PIL.Image模块
		#https://blog.csdn.net/comedate/article/details/121259033
		#https://blog.csdn.net/weixin_44431795/article/details/122016214
		img=QImage(arr.data, arr.shape[1], arr.shape[0], arr.shape[1]*4, QImage.Format_RGBA8888)
		return QPixmap(img)

