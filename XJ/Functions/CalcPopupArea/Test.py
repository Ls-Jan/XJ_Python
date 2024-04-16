__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .CalcPopupArea import CalcPopupArea
from ..GetScreensArea import GetScreensArea

from PyQt5.QtWidgets import QApplication,QPushButton,QMenu,QWidgetAction,QSizePolicy
from PyQt5.QtCore import QEvent, QTimerEvent, Qt,QSize,QPoint,QRect,pyqtSignal
from PyQt5.QtGui import QCursor, QFocusEvent, QShowEvent

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		btn=QPushButton('左键点击弹出菜单')
		menu=QMenu(btn)
		menu.addAction('选项1')
		menu.addAction('选项2')
		menu.addAction('选项3')

		#QMenu支持自定义菜单：https://blog.csdn.net/Black_zy/article/details/116236766
		action=QWidgetAction(menu)
		action.setDefaultWidget(QPushButton("QMenu支持自定义"))
		menu.addAction(action)
		def ShowMenu():
			pos=QCursor().pos()
			# menu.popup(pos)#其实QMenu有自带的弹出功能，不必用户去计算位置

			area=GetScreensArea(includeCursor=True)
			rst=CalcPopupArea(pos,menu.sizeHint(),area,10,True,False,'BTLR')
			# print(pos,rst)
			if(rst):
				menu.setGeometry(rst[2])
			menu.show()
		btn.clicked.connect(ShowMenu)
		self.__btn=btn
	def Opt_Run(self):
		print('其实QMenu有自带的弹出函数QMenu.popup(QPoint)，用户不必去计算弹窗位置')
		print('但为了显得我写的CalcPopupArea稍微有点用，我通过CalcPopupArea将菜单弹出到其他位置而不是默认鼠标角落')
		self.__btn.resize(600,300)
		self.__btn.show()
		self.__btn.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		super().Opt_Run()
		return self.__btn



