
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_PureColorIcon import XJQ_PureColorIcon
from ...Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QCursor

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		btn=QPushButton("ABC")	
		self.__btn=btn

		btn.setStyleSheet('font-size:50px;color:#FFFF00;background:#FF8844')
		btn.setIconSize(QSize(64,64))
		btn.setCursor(QCursor(Qt.ForbiddenCursor))
		# btn.setCursor(QCursor(Qt.PointingHandCursor))

	def Opt_Run(self):
		path=GetRealPath('../../Icons/云下载.png')
		# path=GetRealPath('../../Icons/Arrow/V左箭头.png')
		icon=XJQ_PureColorIcon(path,squareSize=False)
		icon.Set_Color(fg=(0,0,255,192))

		self.__btn.show()
		self.__btn.resize(200,self.__btn.height())
		icon.Set_Color(wid=self.__btn)#根据控件设置icon颜色(在控件显示后控件样式表才会应用生效于调色板中)。通过该方法设置图标颜色的效果有时不理想
		self.__btn.setIcon(icon)#发生变化的icon需要重新调用wid.setIcon(icon)才能生效

		return super().Opt_Run()







