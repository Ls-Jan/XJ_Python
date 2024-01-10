

from PyQt5.QtWidgets import QLabel,QVBoxLayout,QHBoxLayout,QWidget,QGridLayout

from .XJQ_Tag import *
from .XJQ_Marquee import *

__all__=['XJQ_ListViewItem']
class XJQ_ListViewItem(QLabel):#主要为XJQ_ListView服务
	'''
		主要为XJQ_ListView服务，是字串型列表单元内容的扩充
		有四个关键属性：标题、单元色、标签、额外图标
		这四个属性足以覆盖通常应用场景
	'''
	def __init__(self,title,tags,itemColor,extraIcons=[]):
		super().__init__()
		lb=QLabel(title,self)
		lb.setStyleSheet('''
			color:rgba(128,192,192,240);
			background:transparent;
			font-size:25px;
			font-weight:bold;
		''')

		mqTags=XJQ_Marquee(QWidget(),blankPercent=0.15)
		hbox_tag=QHBoxLayout(mqTags.Get_Widget())
		hbox_icons=QHBoxLayout()
		hbox_tag.setSpacing(3)
		hbox_tag.setContentsMargins(0,0,0,0)
		grid=QGridLayout(self)
		grid.addWidget(lb,0,0,1,1)
		grid.addWidget(mqTags,2,0,1,1)
		grid.addLayout(hbox_icons,0,1,3,1)
		grid.setColumnStretch(0,1)
		grid.setContentsMargins(10,4,0,0)
		grid.setSpacing(0)
		self.__lb=lb
		self.__tags=[]
		self.__icons=[]
		self.__tagsBox=hbox_tag
		self.__iconsBox=hbox_icons
		self.Opt_Change(title,tags,itemColor,extraIcons)
	def __SetMarkColor(self,itemColor):
		styleSheet='''
				.XJQ_ListViewItem{
					background:qlineargradient(x1:0, y1:0, x2:1, y2:0,
					stop:0 $col, 
					stop:0.04 rgba(0,0,0,0), 
					stop:1 rgba(0,0,0,0));
				}'''
		styleSheet=styleSheet.replace('$col',itemColor)
		self.setStyleSheet(styleSheet)
	def Opt_Change(self,title=None,tags=None,itemColor=None,extraIcons=None):
		if(title):
			self.__lb.setText(title)
		if(itemColor):
			self.__SetMarkColor(itemColor)
		if(tags):
			count=len(self.__tags)-len(tags)
			while(count>0):
				tag=self.__tags.pop()
				self.__tagsBox.removeWidget(tag)
				count-=1
			while(count<0):
				tag=XJQ_Tag(self,'',XJQ_Tag.Style.Blue,20)
				self.__tagsBox.insertWidget(len(self.__tags),tag)
				self.__tags.append(tag)
				count+=1
			for i in range(len(tags)):
				self.__tags[i].Set_Text(tags[i])
		if(extraIcons!=None):
			while(self.__icons):
				icon=self.__icons.pop()
				self.__tagsBox.removeWidget(icon)
			for icon in extraIcons:
				lb=QLabel()
				lb.setPixmap(icon.pixmap())
				self.__iconsBox.insertWidget(len(self.__icons),lb)
				self.__icons.append(lb)

		# if(extraIcons):
		# icon.pixmap(QSize(25,25))
		# lb.setPixmap()
		# btn.setIconSize(QSize(100,100))

