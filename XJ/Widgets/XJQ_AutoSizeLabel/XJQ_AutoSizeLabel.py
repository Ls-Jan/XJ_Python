__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_AutoSizeLabel']

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap,QMovie

class XJQ_AutoSizeLabel(QLabel):
	'''
		大小自适应的QLabel。
		控件会缩放，图片也会最适缩放。
	'''
	def __init__(self):
		super().__init__()
		self.__autoSize=False
		self.__scaleRateMax=1
		self.__pix=None
		self.__mv=None
		self.__originSize=None#初始大小
		self.__resizeIgnore=False
	def Set_AutoSize(self,flag:bool):
		'''
			控件大小自适应，建议同时调用setMaximumSize/setMinimum以限制最大最小尺寸。
			flag为真时会根据图片进行大小调整。
		'''
		self.__autoSize=flag
		self.update()
	def Set_PictResize(self,scaleRateMax:float):
		'''
			图片大小缩放限制，事实上当图片过大时会无条件的将其缩小，所以此处只讨论图片过小时的放大行为。
			在图片过小时，会根据scaleRateMax对图片进行放大，特别的，如果该值小于1则视为最大化放大。
		'''
		self.__scaleRateMax=scaleRateMax if scaleRateMax>=1 else 1<<31#如果传入的scaleRateMax无效，则取一个非常大的数作为替代
		self.update()
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
	def setMovie(self,mv:QMovie):
		if(mv.currentFrameNumber()<0):
			mv.jumpToFrame(0)
		self.__pix=None
		self.__mv=mv
		self.__originSize=mv.currentPixmap().size()
		super().setMovie(mv)
	def setText(self,tx:str):
		self.__pix=None
		self.__mv=None
		self.__originSize=None
		super().setText(tx)
	def resizeEvent(self,event):
		pix=self.__pix
		mv=self.__mv
		size=self.__originSize

		if(size):#有内容物，进行大小修正
			if(self.__resizeIgnore):
				self.__resizeIgnore=False
			elif(self.__autoSize):#根据内容物调整控件大小
				rateUp=self.__Get_ScaledRate(size,self.minimumSize(),False)
				rateDown=self.__Get_ScaledRate(size,self.maximumSize(),True)
				rateUp=min(1,rateUp,self.__scaleRateMax)
				rateDown=max(1,rateDown)
				rate=rateUp if rateUp>1 else rateDown if rateDown<1 else 1
				rSize=size*rate
				if(rSize!=self.size()):
					self.__resizeIgnore=True
					self.resize(rSize)
					return
			if(True):#根据控件调整内容物大小
				rate=self.__Get_ScaledRate(size,self.size(),True)
				rate=min(rate,self.__scaleRateMax)
				if(rate!=1):
					rSize=size*rate
					if(pix):
						super().setPixmap(pix.scaled(rSize))
					else:
						mv.setScaledSize(rSize)



