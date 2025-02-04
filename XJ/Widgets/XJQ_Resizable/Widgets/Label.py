

from ._Base import Base
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt



class Label(QLabel,Base):
	def __init__(self,*args):
		super().__init__(*args)
		self.__aspectRatio=True
	def __pixmap(self):
		pix=self.pixmap()
		if(not pix):
			mv=self.movie()
			if(mv):
				pix=mv.currentPixmap()
		if(pix and not pix.isNull()):
			if(self.hasScaledContents()):
				sz=self.contentsRect().size()
				pix=pix.scaled(pix.size().scaled(sz,Qt.AspectRatioMode.KeepAspectRatio) if self.__aspectRatio else sz)
		return pix
	def paintEvent(self,event:QPaintEvent):
		#见源码：https://codebrowser.dev/qt6/qtbase/src/widgets/widgets/qlabel.cpp.html#_ZN6QLabel10paintEventEP11QPaintEvent
		ptr=self.painter()
		style=self.style()
		rect=self.scaleRect(self.rect())
		pix=self.__pixmap()
		if(pix):
			style.drawItemPixmap(ptr,rect,Qt.AlignmentFlag.AlignCenter,pix)
		else:
			style.drawItemText(ptr,rect,Qt.AlignmentFlag.AlignCenter,self.palette(),True,self.text())
	def setAspectRatio(self,flag:bool):
		'''
			设置缩放图片(setScaledContents)时是否固定宽高比
		'''
		self.__aspectRatio=flag
