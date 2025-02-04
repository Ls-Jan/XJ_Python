

from ._Base import Base
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QPushButton,QStyleOptionButton,QStyle

class PushButton(QPushButton,Base):
	def __init__(self,*args):
		super().__init__(*args)
	def paintEvent(self,event:QPaintEvent):
		ptr=self.painter()
		style=self.style()
		rect=self.scaleRect(self.rect())
		opt=QStyleOptionButton()
		self.initStyleOption(opt)
		opt.rect=rect
		style.drawControl(QStyle.ControlElement.CE_PushButton,opt,ptr,self)


