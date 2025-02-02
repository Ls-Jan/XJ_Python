

from .BaseFrameChange import BaseFrameChange,QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize

class FrameChange_Label(BaseFrameChange):
	def __init__(self,lb:QLabel,size:QSize):
		super().__init__()
		self.__lb=lb
		self.__sz=size
	def __call__(self,pix:QPixmap,type:BaseFrameChange.Type):
		super().__call__(pix,type)
		if(self.__sz):
			pix=pix.scaled(self.__sz)
		self.__lb.setPixmap(pix)

