
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtWidgets import QWidget,QPushButton,QBoxLayout,QLabel,QSizePolicy
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QPixmap

__all__=['XJQ_FolderBox']
class XJQ_FolderBox(QWidget):#折叠型容器
	'''
		折叠型容器，行为可参考QToolBox，
		但QToolBox说实话已经落伍了，而且控件行为难以管制，例如一直会并且也只会展开一项
		本控件搭配QBoxLayout、QScrollArea效果更佳
	'''
	__content=None
	__title=None

	__tx=None
	__icon=None
	__iconData={#麻烦的一批，不知道起啥名索性扔字典里
		'size':QSize(16,16),
		'sClose':None,
		'sOpen':None,
		'close':None,
		'open':None,
	}
	def __init__(self,titleTx:str=None,direction:QBoxLayout.Direction=QBoxLayout.TopToBottom):
		'''
			设置标题以及展开方向
		'''
		super().__init__()
		content=QWidget()
		title=QPushButton()
		tx=QLabel(titleTx)
		icon=QLabel()
		box=QBoxLayout(direction,self)
		box.addWidget(title)
		box.addWidget(content)
		box.addStretch(1)
		box.setContentsMargins(0,0,0,0)
		# content.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		self.__title=title
		self.__tx=tx
		self.__icon=icon
		self.__content=content
		for key in ['sClose','sOpen','close','open']:
			self.__iconData[key]=QPixmap()
		self.Set_TitleLayout(self.Get_DefaultTitleLayout)
	def Get_IsExpand(self):
		'''
			获取当前展开状态
		'''
		return self.__content.isVisible()
	def Get_Content(self):
		'''
			获取内容物
		'''
		return self.__content
	def Set_Expand(self,flag:bool=None):
		'''
			设置展开状态，如果为None则反转当前展开状态
		'''
		if(flag==None):
			flag=not self.__content.isVisible()
		self.__content.setVisible(flag)
		self.__icon.setPixmap(self.__iconData['open' if flag else 'close'])
	def Set_Text(self,tx=None):
		'''
			设置标题文本
		'''
		if(tx!=None):
			self.__tx.setText(tx)
	def Set_Icon(self,pixClose:QPixmap=None,pixOpen:QPixmap=None,size:QSize=None):
		'''
			设置标题图标以及图标大小
			不想要Icon直接传入空QPixmap即可
		'''
		if(not size):
			size=self.__iconData['size']
		if(not pixClose):
			pixClose=self.__iconData['sClose']
		if(not pixOpen):
			pixOpen=self.__iconData['sOpen']
		self.__iconData['size']=size
		self.__iconData['sClose']=pixClose
		self.__iconData['sOpen']=pixOpen
		self.__iconData['close']=QPixmap() if pixClose.isNull() else pixClose.scaled(size)
		self.__iconData['open']=QPixmap() if pixOpen.isNull() else pixOpen.scaled(size)
		self.Set_Expand(self.__content.isVisible())
	def Set_TitleLayout(self,createLayout):
		'''
			默认布局不满意？自己设置！createLayout格式参考Get_DefaultTitleLayout
		'''
		box=self.layout()
		layout=createLayout(self.__tx,self.__icon,box.direction())
		newTitle=QPushButton()
		newTitle.setStyleSheet(self.__title.styleSheet())
		newTitle.setLayout(layout)
		newTitle.clicked.connect(self.Set_Expand)
		newTitle.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		box.removeWidget(self.__title)
		box.insertWidget(0,newTitle)
		self.__title=newTitle
	def Set_TitleStyle(self,style):
		'''
			设置标题文本样式
		'''
		self.__title.setStyleSheet(style)
	def Set_Content(self,wid):
		'''
			设置内容物
		'''
		self.__content=wid
	@staticmethod
	def Get_DefaultTitleLayout(tx:QLabel,icon:QLabel,boxDirection:QBoxLayout.Direction):
		'''
			获取标题栏默认布局(盒布局)，控件tx和icon会加入到本布局中
		'''
		V,H=0,0
		if(boxDirection==QBoxLayout.TopToBottom or boxDirection==QBoxLayout.BottomToTop):
			direction=QBoxLayout.LeftToRight
			H=10
		else:
			direction=QBoxLayout.TopToBottom
			V=10
		box=QBoxLayout(direction)
		box.addStretch(1)
		box.addWidget(icon)
		if(tx.text()):
			box.insertWidget(0,tx)
		else:
			box.insertStretch(box.count(),1)
		box.setContentsMargins(H,V,H,V)
		box.setAlignment(Qt.AlignCenter)
		return box



