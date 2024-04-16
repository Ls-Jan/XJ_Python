
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_MouseTriggerBox import XJQ_MouseTriggerBox

from PyQt5.QtWidgets import QPushButton,QWidget,QLabel,QListView,QHBoxLayout
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QStandardItemModel,QStandardItem

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		win=QPushButton("移动鼠标")
		t=XJQ_MouseTriggerBox(win)
		btn=QPushButton("Test",t)

		t.Opt_AddArea('矩形-百分数',QRectF(0.25,0.25,0.5,0.5))
		t.Opt_AddArea('矩形-固定值',QRectF(0,0,100,100))
		t.Opt_AddArea('按钮',btn)
		t.enter.connect(lambda name,flag:print('进入' if flag else '离开',name))
		t.hover.connect(lambda name,flag:print('显示Tooltip' if flag else '隐藏Tooltip',name))
		btn.setGeometry(100,100,100,100)
		self.__win=win
	def Opt_Run(self):
		print('添加了三块区域，分别是')
		print('【按钮】')
		print('【矩形-百分数[QRectF(0.25,0.25,0.5,0.5)]】')
		print('【矩形-固定值[QRectF(0,0,100,100)]】')
		print('移动鼠标进行尝试')
		print('\n'*3)

		self.__win.resize(600,400)
		self.__win.show()
		super().Opt_Run()
		# return self.__win





