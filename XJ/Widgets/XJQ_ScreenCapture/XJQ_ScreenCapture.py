__author__='Ls_Jan'
__version__='1.0.0'
__all__=['XJQ_ScreenCapture']

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal,QSize
from PyQt5.QtWidgets import QApplication
from typing import Union

from ..XJQ_ScreenAreaSelector import XJQ_ScreenAreaSelector
from ..XJQ_AutoSizeLabel import XJQ_AutoSizeLabel
from ...Functions.GetRealPath import GetRealPath

class XJQ_ScreenCapture(XJQ_AutoSizeLabel):
	'''
		截屏按钮，点击即截屏，
		截屏后会发送信号captured(QPixmap)
	'''
	captured=pyqtSignal(QPixmap)
	def __init__(self,icon:Union[QPixmap,str]=None,size:QSize=QSize(128,128),minSize:QSize=QSize(64,64)):
		'''
			接受一个截屏图标，可传入文件路径或是QPixmap对象，如果传入空则使用默认图标。
			size为控件图标大小，minSize为控件最小大小。
		'''
		super().__init__()
		if(icon==None):
			icon=GetRealPath('./图标-截图.ico')
		if(isinstance(icon,str)):
			icon=QPixmap(icon)
		self.setPixmap(icon.scaled(size))
		self.setMinimumSize(minSize)
		sa=XJQ_ScreenAreaSelector()
		sa.Set_QuickSelect(True)
		sa.selected.connect(self.__Opt_CaptureFinish)
		self.__sa=sa
		self.__clipboard=False
	def Set_CopyToClipboard(self,flag:bool):
		'''
			是否将图片复制到剪切板，
			如果为真则在截屏结束后会设置剪切板的内容
		'''
		self.__clipboard=flag
	def Set_QuickSelect(self,flag:bool):
		'''
			快速截屏，左键抬起就结束
		'''
		self.__sa.Set_QuickSelect(flag)
	def Opt_StartCapture(self):
		'''
			开始截屏
		'''
		self.__sa.show()
	def mousePressEvent(self,event):
		self.Opt_StartCapture()
	def __Opt_CaptureFinish(self):
		pix=self.__sa.Get_Screenshot()
		self.__sa.hide()
		self.__sa.Opt_Clear()
		if(pix):
			if(self.__clipboard):
				QApplication.clipboard().setPixmap(pix)
			self.captured.emit(pix)

