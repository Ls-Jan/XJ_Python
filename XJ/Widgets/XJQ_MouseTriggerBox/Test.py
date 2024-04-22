
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_MouseTriggerBox import XJQ_MouseTriggerBox

from PyQt5.QtWidgets import QPushButton,QWidget,QLabel,QListView,QHBoxLayout
from PyQt5.QtCore import QRectF,Qt
from PyQt5.QtGui import QPainter,QPen,QColor

__all__=['Test']

class TestWidget(QLabel):
	def __init__(self,*args):
		super().__init__(*args)
		self.__area={}
		self.setAlignment(Qt.AlignCenter)
	def Opt_AddArea(self,name:str,area:QRectF=None):
		if(isinstance(area,QRectF)):
			self.__area[name]=area
			self.update()
	def paintEvent(self,event) -> None:
		super().paintEvent(event)
		ptr=QPainter(self)
		ptr.setPen(QPen(QColor(0,192,255),4))
		for name,area in self.__area.items():
			attrs=['left','top','right','bottom']
			size=[self.width(),self.height()]
			area=QRectF(area)
			for i in range(len(attrs)):
				attr=attrs[i]
				val=getattr(area,attr)()
				if(0<=val<=1):
					val=val*size[i%2]
					getattr(area,'set'+attr.capitalize())(val)#py字符串首字母大写：str.capitalize
			area=area.toRect()
			ptr.drawRect(area)

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=TestWidget("移动鼠标")
		mt=XJQ_MouseTriggerBox(win,True)
		btn=QPushButton("区域-按钮")

		mt.enter.connect(lambda name,flag:print(name,'区域', '√' if flag else 'x'))
		mt.hover.connect(lambda name,flag:print(name,'Tooltip','√' if flag else 'x'))
		btn.setMinimumSize(150,100)
		hbox=QHBoxLayout(mt)
		hbox.addStretch(1)
		hbox.addWidget(btn,1)
		hbox.addStretch(6)
		for item in [('区域-百分数',QRectF(0.25,0.25,0.1,0.6)),('区域-固定值',QRectF(0,0,100,100)),('区域-小按钮',btn)]:
			mt.Opt_AddArea(*item)
			win.Opt_AddArea(*item)

		self.__win=win
	def Opt_Run(self):
		print('有三种添加触发区的方式')
		print('移动鼠标进行尝试')
		print('可改动窗口大小以感受效果')
		print('\n'*3)

		self.__win.resize(600,400)
		self.__win.show()
		super().Opt_Run()
		return self.__win

