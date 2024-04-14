
__version__='1.0.0'
__author__='Ls_Jan'

from ..XJQ_SwitchBtn import XJQ_SwitchBtn
from ..XJQ_PureColorIconButton import XJQ_PureColorIconButton
from ..XJQ_LocateBox import XJQ_LocateBox
from ..XJQ_AnimateShowHideBox import XJQ_AnimateShowHideBox
from ...Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt

__all__=['OperationUI']
class OperationUI:
	'''
		很简单的UI，只为XJQ_Clock服务
	'''
	btnPlay=None
	btnQuit=None
	def __init__(self,parent,iconPause:str=GetRealPath('./暂停.png'),iconPlay:str=GetRealPath('./播放.png'),iconQuit:str=GetRealPath('./停止.png')):
		btnPlay=XJQ_SwitchBtn(XJQ_PureColorIconButton(iconPlay),XJQ_PureColorIconButton(iconPause))
		btnQuit=XJQ_PureColorIconButton(iconQuit)

		wid=QFrame()
		lbox=XJQ_LocateBox(wid)
		lbox.Opt_AddWidget(btnPlay,Qt.AlignCenter)
		lbox.Opt_AddWidget(btnQuit,Qt.AlignVCenter|Qt.AlignRight,(0,0))
		shbox=XJQ_AnimateShowHideBox(parent)
		shbox.Set_Content(wid)
		self.btnPlay=btnPlay
		self.btnQuit=btnQuit
		self.__parent=parent
		self.__shbox=shbox
		self.resize()
		self.hide()
	def setStyleSheet(self,qss:str):
		self.__shbox.Get_Content().setStyleSheet(qss)
	def resize(self):
		size=self.__parent.size()
		self.__shbox.resize(size)
		size=size.boundedTo(size.transposed())#最小正方形
		self.btnPlay.resize(size/1.2)
		self.btnQuit.resize(size/1.6)
	def show(self):
		self.resize()
		if(not (self.btnPlay.isHidden() and self.btnQuit.isHidden())):
			self.__shbox.show()
	def hide(self):
		self.__shbox.hide()


