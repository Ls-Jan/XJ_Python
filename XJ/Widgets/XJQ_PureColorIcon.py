

__version__='1.0.0'
__author__='Ls_Jan'


import cv2
import numpy as np
from typing import Union#与py的“类型注解”用法有关：https://zhuanlan.zhihu.com/p/419955374
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QIcon,QPixmap,QImage,QPalette,QColor

__all__=['XJQ_PureColorIcon']
class XJQ_PureColorIcon(QIcon):#纯色图标
	'''
		纯色图标，可改图标色以及背景色，以及可以预置/修改图标大小(调用pixmap函数时可不必再传入大小参数了)。
		当然，类似QPushButton在调用setIcon后，icon发生更新时QPushButton显示的图标并不会发生改变，需要再次调用setIcon才行
	'''
	def __init__(self,
			  data:Union[str,np.ndarray,QIcon,QPixmap,QImage],
			  fg:tuple=(0,255,0,255),
			  bg:tuple=(0,0,0,0),
			  size:tuple=(20,20),
			  hint=None,
			  squareSize=True):
		'''
			data可以是
				图片路径(str)
				图片数据(np.ndarray)
				图标类(QIcon/XJQ_PureColorIcon)
				图片类(QPixmap/QImage)
				None
			size设置图标大小，特殊场合有用(例如在调用pixmap()时如果缺省参数那么将以size为准
			hint额外信息补充，在特殊场合下有用
			squareSize若为真，则设置图标大小时会强制调整为正方形大小
		'''
		# QIcon：https://doc.qt.io/qt-6/qicon.html
		super().__init__()
		if(isinstance(data,str)):
			try:
				im=self.Opt_LoadPictAsArray(data)
			except:
				raise Exception(f'路径{data}不存在')
		elif(isinstance(data,np.ndarray)):
			im=data
		elif(data==None or isinstance(data,QIcon)):
			if(data==None):
				data=QIcon()
			s=data.availableSizes()
			if(s):
				im=data.pixmap(s[0])
			else:
				im=QPixmap(1,1)
				im.fill(Qt.transparent)
			im=self.Trans_PixmapToArray(im)
		elif(isinstance(data,QImage) or isinstance(data,QPixmap)):
			im=self.Trans_PixmapToArray(QPixmap(data))
		else:
			raise Exception('data参数错误，类型仅能为np.ndarray(图片数据)或是str(图片路径)或是QIcon/XJQ_PureColorIcon或是QPixmap或是None')

		try:
			if(len(fg)==3):
				fg=(*fg,255)
			if(len(bg)==3):
				bg=(*bg,255)
			msk=cv2.split(im)[3]
			self.__msk=cv2.threshold(msk,127,255,cv2.THRESH_BINARY)[1]
			#cv2纯色图：https://blog.csdn.net/qq_45666248/article/details/107666586
			self.__bg=np.zeros((*msk.shape,4),np.uint8)
			self.__fg=np.zeros((*msk.shape,4),np.uint8)
			self.__bg[:] = bg
			self.__fg[:] = fg
			self.__squareSize=squareSize
			self.__size=QSize()
			self.__hint=hint
			self.__UpdatePixmap()
			self.resize(*size)
		except:
			raise Exception('转换失败！data数据错误！')
	def Set_Color(self,fg:Union[QColor,tuple]=None,bg:Union[QColor,tuple]=None,wid=None):
		'''
			设置前景背景色。
			如果指定wid那么将根据wid来决定前景背景色(别用wid方法指定颜色，不靠谱，时灵时不灵)
		'''
		if(wid!=None):
			#获取控件颜色(本质获取调色板)：https://blog.csdn.net/c_shell_python/article/details/98895712
			pt=wid.palette()
			fg=pt.text().color()
			# bg=pt.button().color()
			bg=pt.base().color()
			cols=list(map(lambda col:[getattr(col,ch)() for ch in ['red','green','blue','alpha']],[fg,bg]))
			self.__fg[:] = cols[0]
			self.__bg[:] = cols[1]
		else:
			if(fg!=None):
				if(isinstance(fg,QColor)):
					fg=self.Trans_QColorToList(fg)
				elif(len(fg)==3):
					fg=(*fg,255)
				self.__fg[:] = fg
			if(bg!=None):
				if(isinstance(bg,QColor)):
					bg=self.Trans_QColorToList(bg)
				elif(len(bg)==3):
					bg=(*bg,255)
				self.__bg[:] = bg
		self.__UpdatePixmap()
	def pixmap(self,*arg):
		'''
			获取QPixmap对象，如果无参数那么以默认size为准
		'''
		if(arg):
			return super().pixmap(*arg)
		pix=super().pixmap(self.__size)
		if(not pix.isNull()):#如果不判空就调用scaled的话会有烦人的警告输出
			pix=pix.scaled(self.__size)#调用scaled强制放大
		return pix
	def size(self):
		'''
			特殊场合有用
		'''
		return self.__size
	def resize(self,*size):
		'''
			设置size值，特殊场合有用
			调用方式可以是resize(32,32)或是resize(QSize(32,32))
		'''
		if(len(size)>1):
			size=QSize(*size)
		else:
			size=size[0]
		if(self.__squareSize):
			size=size.boundedTo(size.transposed())#最小正方形
		self.__size=size
	def hint(self):
		'''
			获取补充信息，特殊场合有用
		'''
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
	def Trans_QColorToList(col):
		return [getattr(col,key)() for key in ['red','green','blue','alpha']]
	@staticmethod
	def Trans_ArrayToPixmap(arr):#arr对应四通道图片。不使用PIL.Image模块
		#https://blog.csdn.net/comedate/article/details/121259033
		#https://blog.csdn.net/weixin_44431795/article/details/122016214
		img=QImage(arr.data, arr.shape[1], arr.shape[0], arr.shape[1]*4, QImage.Format_RGBA8888)
		return QPixmap(img)
	@staticmethod
	def Trans_PixmapToArray(pix):#pix是RGBA四通道QPixmap。不使用PIL.Image模块
		#https://deepinout.com/numpy/numpy-questions/700_numpy_qimage_to_numpy_array_using_pyside.html#ftoc-heading-3
		h,w=pix.height(),pix.width()
		buffer = QImage(pix).constBits()
		buffer.setsize(h*w*4)
		arr = np.frombuffer(buffer, dtype=np.uint8).reshape((h,w,4))
		return arr.copy()

