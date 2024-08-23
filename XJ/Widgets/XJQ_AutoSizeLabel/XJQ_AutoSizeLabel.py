__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_AutoSizeLabel']

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QPixmap,QMovie

class XJQ_AutoSizeLabel(QLabel):
	'''
		大小自适应的QLabel，图片会最适缩放。
		默认使用了居中对齐(Qt.AlignmentFlag.AlignCenter)，可根据实际需要去调用QLabel.setAlignment进行修改；
		不建议调用QWidget.setSizePolicy修改大小策略；
	'''
	def __init__(self):
		super().__init__()
		self.__scaleRateMax=1
		self.__pix=None
		self.__mv=None
		self.__originSize=QSize()#初始大小
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
	def Set_PictResize(self,scaleRateMax:float):
		'''
			图片大小缩放限制，事实上当图片过大时会无条件的将其缩小，所以此处只讨论图片过小时的放大行为。
			在图片过小时，会根据scaleRateMax对图片进行放大，特别的，如果该值小于1则视为最大化放大。
		'''
		self.__scaleRateMax=scaleRateMax if scaleRateMax>=1 else 1<<31#如果传入的scaleRateMax无效，则取一个非常大的数作为替代
		self.update()
	def sizeHint(self):
		return self.__originSize
	def minimumSizeHint(self):
		return QSize(24,24)#再小就看不见辣
	@staticmethod
	def __Get_ScaledRate(szSource:QSize,szLimit:QSize,inside:bool):
		'''
			将szSource进行等比缩放并返回最适缩放比。
			inside为真则szSource的宽高不大于szLimit；
			inside为假则szSource的宽高不小于szLimit；
		'''
		limW,limH=szLimit.width(),szLimit.height()
		srcW,srcH=szSource.width(),szSource.height()
		rateW=1 if(limW<=0 or srcW<=0) else limW/srcW
		rateH=1 if(limH<=0 or srcH<=0) else limH/srcH
		rate=min(rateW,rateH) if inside else max(rateW,rateH)
		return rate
	def setPixmap(self,pix:QPixmap):
		self.__pix=pix
		self.__mv=None
		self.__originSize=pix.size()
		super().setPixmap(pix)
		self.__Opt_Update()
	def setMovie(self,mv:QMovie):
		self.__pix=None
		self.__mv=mv
		if(mv.currentFrameNumber()<0):
			mv.jumpToFrame(0)
		self.__originSize=mv.currentPixmap().size()
		super().setMovie(mv)
	def setText(self,tx:str):
		self.__pix=None
		self.__mv=None
		self.__originSize=QSize()
		super().setText(tx)
	def resizeEvent(self,event):
		self.__Opt_Update()
	def __Opt_Update(self):
		pix=self.__pix
		mv=self.__mv
		size=self.__originSize
		if(not size.isEmpty()):#有内容物，进行大小修正。不使用bool(size)是因为它会等效于size.isValid()，即使是QSize(0,0)也会返回真，属实恶趣味
			#根据控件调整内容物大小
			rate=self.__Get_ScaledRate(size,self.size(),True)
			rate=min(rate,self.__scaleRateMax)
			if(True):
				rSize=size*rate
				if(pix):
					if(super().pixmap().size()!=rSize):
						super().setPixmap(pix.scaled(rSize))
				else:
					mv.setScaledSize(rSize)


