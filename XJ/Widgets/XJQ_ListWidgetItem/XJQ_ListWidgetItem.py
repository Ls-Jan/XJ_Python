
__version__='1.1.0'
__author__='Ls_Jan'

from ..XJQ_Tag import XJQ_Tag
from ..XJQ_MarqueeBox import XJQ_MarqueeBox
from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager
from ...Functions.GetRealPath import GetRealPath
from ...Functions.QColorToRGBA import QColorToRGBA

from PyQt5.QtWidgets import QLabel,QHBoxLayout,QWidget,QGridLayout
from PyQt5.QtGui import QColor

__all__=['XJQ_ListWidgetItem']
class XJQ_ListWidgetItem(QLabel):#主要为XJQ_ListWidget服务
	'''
		主要为XJQ_ListWidget服务，是字串型列表单元内容的扩充
		有四个关键属性：标题、单元色、标签、额外图标
		这四个属性足以覆盖通常应用场景
		标签具有跑马灯功能
	'''
	__qssManager=None#使用公用的qss管理
	def __init__(self,
			  title:str,
			  tags:list=None,
			  itemColor:str=None,
			  extraIcons:list=None):
		'''
			title：标题
			tags：标签
			itemColor：单元色(该值将插入样式表中)
			extraIcons：额外图标
		'''
		super().__init__()
		if(self.__qssManager==None):
			sm=XJQ_StyleSheetManager()
			sm.setStyleSheet(GetRealPath('./styleSheet.qss'),multi=True)
			self.__class__.__qssManager=sm
		title=QLabel(title,self)
		mqTags=XJQ_MarqueeBox(QWidget(),blankPercent=0.15)
		hbox_tag=QHBoxLayout(mqTags.Get_Widget())
		hbox_icons=QHBoxLayout()
		hbox_tag.setSpacing(3)
		hbox_tag.setContentsMargins(0,0,0,0)
		grid=QGridLayout(self)
		grid.addWidget(title,0,0,1,1)
		grid.addWidget(mqTags,2,0,1,1)
		grid.addLayout(hbox_icons,0,1,3,1)
		grid.setColumnStretch(0,1)
		grid.setContentsMargins(10,4,0,0)
		grid.setSpacing(0)
		self.__title=title
		self.__tags=[]
		self.__icons=[]
		self.__itemColor=QColor(0,0,0,0)
		self.__style={'main':'Main','itemColor':'ItemColor','title':'Title'}
		self.__tagsBox=hbox_tag
		self.__iconsBox=hbox_icons
		self.Opt_Change(None,tags,itemColor,extraIcons)
		self.update()
	@classmethod
	def Set_NewStyle(self,name:str,qss:str,clear:bool=False):
		'''
			注册新的样式表，qss可以是路径。
			如果name直接传None则加载qss中的复数个样式表(此时qss可为文件路径)。
			clear为真时将无视name和qss，重置样式表数据

			特别的，该函数调用后不会立即生效，需对实际控件调用update刷新状态
		'''
		sm=self.__qssManager
		if(clear):
			sm.setStyleSheet('',clear=True)
			qss=GetRealPath('./styleSheet.qss')
		return self.__qssManager.setStyleSheet(qss,name)
	def update(self,*args):
		sm=self.__qssManager
		self.__title.setStyleSheet(sm.styleSheet(self.__style['title']))
		self.setStyleSheet(sm.styleSheet(self.__style['main'])+sm.styleSheet(self.__style['itemColor']).replace('--col',QColorToRGBA(self.__itemColor,True)))
		super().update(*args)
	def Set_Style(self,main:str=None,itemColor:str=None,title:str=None):
		'''
			设置样式
		'''
		for item in [('main',main),('itemColor',itemColor),('title',title)]:
			if(item[1]):
				self.__style[item[0]]=item[1]
	def Opt_Change(self,
				title:str=None,
				tags:list=None,
				itemColor:QColor=None,
				extraIcons:list=None):
		'''
			title：标题
			tags：标签
			itemColor：单元色(该值将插入样式表中)
			extraIcons：额外图标
		'''
		if(title):
			self.__title.setText(title)
		if(itemColor):
			self.__itemColor=itemColor
			self.setStyleSheet(self.__qssManager.styleSheet(self.__style['main'])+self.__qssManager.styleSheet(self.__style['itemColor']).replace('--col',QColorToRGBA(itemColor,True)))
		if(tags):
			count=len(self.__tags)-len(tags)
			while(count>0):
				tag=self.__tags.pop()
				self.__tagsBox.removeWidget(tag)
				count-=1
			while(count<0):
				tag=XJQ_Tag('',fontSize=20)
				self.__tagsBox.insertWidget(len(self.__tags),tag)
				self.__tags.append(tag)
				count+=1
			for i in range(len(tags)):
				self.__tags[i].setText(tags[i])
		if(extraIcons!=None):
			while(self.__icons):
				icon=self.__icons.pop()
				self.__tagsBox.removeWidget(icon)
			for icon in extraIcons:
				lb=QLabel()
				lb.setPixmap(icon.pixmap())
				self.__iconsBox.insertWidget(len(self.__icons),lb)
				self.__icons.append(lb)
