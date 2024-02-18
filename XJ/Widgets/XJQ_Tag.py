from enum import Enum
from typing import Union
from PyQt5.QtWidgets import QLabel,QPushButton,QSizePolicy,QWidget
from PyQt5.QtCore import pyqtSignal,Qt

__all__=['XJQ_Tag']
class XJQ_Tag(QPushButton):#原先是继承QLabel，后来需要扩展“点击”效果，只能换成QPushButton了
	'''
		颜色风格参考了Element-plus的按钮样式：https://element-plus.org/zh-CN/component/button.html
		标签可点击，点击后会触发clicked信号

		标签样式在XJQ_Tag.Style中提供，目前有五种颜色：蓝红绿灰橙
		当然，对目前的样式不满的可以自行传入其他样式
	'''
	clicked=pyqtSignal(bool)#提供一个点击信号槽，参数为活跃状态
	class Style(Enum):#别问，问就是一点一点试的。我也想扒样式表但不知道哪里才有。
		Base='''
			border-width:2px;
			border-style:solid;
			border-radius: 10px;
			padding:1px 2px;
			'''

		Blue='''
			background:rgba(0,127,255,32);
			color:rgba(64,127,255,224);
			border-color:rgba(0,128,255,192);
			'''
		BlueActive='''
			background:rgba(0,127,255,80);
			color:rgba(96,160,255,255);
			border-color:rgba(0,128,255,224);
			'''
		BlueHover='''
			background:rgba(0,127,255,128);
			'''
		BluePress='''
			background:rgba(0,127,255,96);
			'''

		Red='''
			background:rgba(255,0,0,32);
			color:rgba(255,64,64,224);
			border-color:rgba(255,32,32,192);
			'''
		RedActive='''
			background:rgba(255,0,0,80);
			color:rgba(255,96,96,255);
			border-color:rgba(255,64,64,244);
			'''
		RedHover='''
			background:rgba(255,0,0,128);
			'''
		RedPress='''
			background:rgba(255,0,0,96);
			'''

		Green='''
			background:rgba(0,255,0,32);
			color:rgba(64,255,64,192);
			border-color:rgba(32,255,32,164);
			'''
		GreenActive='''
			background:rgba(0,255,0,80);
			color:rgba(64,255,64,224);
			border-color:rgba(32,255,32,192);
			'''
		GreenHover='''
			background:rgba(0,255,0,128);
			'''
		GreenPress='''
			background:rgba(0,255,0,96);
			'''

		Gray='''
			background:rgba(144,144,144,64);
			color:rgba(128,128,128,224);
			border-color:rgba(128,128,128,192);
			'''
		GrayActive='''
			background:rgba(144,144,144,112);
			color:rgba(192,192,192,224);
			border-color:rgba(192,192,192,192);
			'''
		GrayHover='''
			background:rgba(144,144,144,160);
			color:rgba(160,160,160,224);
			border-color:rgba(160,160,160,224);
			'''
		GrayPress='''
			background:rgba(144,144,144,80);
			color:rgba(144,144,144,224);
			border-color:rgba(144,144,144,192);
			'''

		Orange='''
			background:rgba(255,156,0,48);
			color:rgba(255,156,0,224);
			border-color:rgba(255,192,128,160);
			'''
		OrangeActive='''
			background:rgba(255,156,0,112);
			color:rgba(255,192,32,224);
			border-color:rgba(255,192,128,224);
			'''
		OrangeHover='''
			background:rgba(255,156,0,144);
			'''
		OrangePress='''
			background:rgba(255,156,0,112);
			'''
	def __init__(self,parent:QWidget,
				  text:str,#文本
				  style=Style.Blue,#基础样式
				  styleHover=None,#鼠标悬浮
				  stylePress=None,#鼠标按下
				  styleActive=None,#活跃
				  fontSize=25,#字体大小
				  clickable=False,):#当该值为真时Tag处于可交互状态，styleHover和styleActive生效，鼠标光标变成手指
		'''
			text：文本
			style：基础样式
			styleHover：悬浮样式
			stylePress：按下样式
			styleActive：活跃样式
			fontSize：字体大小
			clickable：当该值为真时Tag处于可交互状态，styleHover和stylePress生效，鼠标光标变成手指
		'''
		super().__init__(parent)
		self.Set_Text(text)
		self.__active=False
		self.__clickable=clickable
		self.__fontSize=fontSize
		self.__style={'normal':None,'hover':None,'press':None,'active':None}
		self.Set_Style(style,styleHover,stylePress,styleActive)
		self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		self.Set_Clickable(clickable)
	def Set_Active(self,flag:bool):
		'''
			设置当前状态
		'''
		self.__active=flag
		self.__SetStyleSheet()
	def Set_Clickable(self,flag:bool):
		'''
			设置可否点击
		'''
		self.__clickable=flag
		self.setCursor(Qt.PointingHandCursor if flag else Qt.ArrowCursor)
		self.__SetStyleSheet()
	def Set_Text(self,text:str):
		'''
			设置文本，调用setText也一样
		'''
		self.setText(text)
	def Set_FontSize(self,fontSize:int):
		'''
			设置字体大小
		'''
		self.__fontSize=fontSize
		self.__SetStyleSheet()
	def Set_Style(self,
			   style:Union[str,Style],
			   styleHover:Union[str,Style]=None,
			   stylePress:Union[str,Style]=None,
			   styleActive:Union[str,Style]=None):
		'''
			设置样式表，
			除style外的其余三个样式若不指定则会默认使用配套样式，
			例如指定style=Style.Red，那么其余样式会默认指定Style.Red系列，即Style.RedHover、Style.RedPress、Style.RedActive
			特别的，若style是字符串，默认样式采用的是Style.Gray系列

			若提供的Style样式无法满足需求的话可以传入自定义样式表
		'''
		styleDefault=style if isinstance(style,self.Style) else self.Style.Gray
		for key,style in {'Normal':style,'Hover':styleHover,'Press':stylePress,'Active':styleActive}.items():
			if(not(isinstance(style,str) and isinstance(style,self.Style))):
				style=None
			if(not style):
				name=styleDefault.name+key
				if(hasattr(self.Style,name)):
					style=getattr(self.Style,name)
				else:
					style=styleDefault
			if(isinstance(style,self.Style)):
				style=style.value
			self.__style[key.lower()]=style
		self.__SetStyleSheet()
	def __SetStyleSheet(self):
		styleB=self.Style.Base.value
		styleN=self.__style['normal']
		styleP=''
		styleH=''
		fontSize=f'font-size:{self.__fontSize}px;'
		if(self.__clickable):
			if(self.__active):
				styleN=self.__style['active']
			styleH=self.__style['hover']
			styleP=self.__style['press']
		style='''
			.XJQ_Tag{
				styleB
				styleN
				fontSize
			}
			.XJQ_Tag:hover{
				styleH
			}
			.XJQ_Tag:pressed{
				styleP
			}
		'''
		style=style.replace('styleB',styleB)
		style=style.replace('styleN',styleN)
		style=style.replace('styleH',styleH)
		style=style.replace('styleP',styleP)
		style=style.replace('fontSize',fontSize)
		self.setStyleSheet(style)
	def mousePressEvent(self,event):
		if(self.__clickable):
			super().mousePressEvent(event)
			self.Set_Active(not self.__active)
			self.clicked.emit(self.__active)







