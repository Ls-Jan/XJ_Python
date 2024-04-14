
__version__='1.1.0'
__author__='Ls_Jan'

from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager
from ...Functions.GetRealPath import GetRealPath

from typing import Union
from PyQt5.QtWidgets import QPushButton,QSizePolicy,QWidget
from PyQt5.QtCore import pyqtSignal,Qt

__all__=['XJQ_Tag']
class XJQ_Tag(QPushButton):#原先是继承QLabel，后来需要扩展“点击”效果，只能换成QPushButton了
	'''
		颜色风格参考了Element-plus的按钮样式：https://element-plus.org/zh-CN/component/button.html
		标签可点击，点击后会触发clicked信号

		标签样式在XJQ_Tag.Style中提供，目前有五种颜色：蓝红绿灰橙，可通过XJQ_Tag.Get_AvaliableName查看当前可接受的样式，
		当然，对目前的样式不满的可以通过XJQ_Tag.Set_NewStyleSheet自行传入其他样式
	'''
	__qssManager=None#使用公用的qss管理
	clicked=pyqtSignal(bool)#提供一个点击信号槽，参数为活跃状态
	def __init__(self,
				  text:str,#文本
				  style:str="Blue",#基础样式
				  styleHover:str=None,#鼠标悬浮
				  stylePress:str=None,#鼠标按下
				  styleActive:str=None,#活跃
				  fontSize:int=25,#字体大小
				  clickable:bool=False,
				  parent:QWidget=None):#当该值为真时Tag处于可交互状态，styleHover和styleActive生效，鼠标光标变成手指
		'''
			text：文本
			style：基础样式
			styleHover：悬浮样式
			stylePress：按下样式
			styleActive：活跃样式
			fontSize：字体大小
			clickable：当该值为真时Tag处于可交互状态，styleHover和stylePress生效，鼠标光标变成手指
		'''
		super(QPushButton,self).__init__(parent)
		if(self.__qssManager==None):
			sm=XJQ_StyleSheetManager()
			sm.setStyleSheet(GetRealPath('./styleSheet.qss'),multi=True)
			self.__class__.__qssManager=sm
		self.setText(text)
		self.__active=False
		self.__clickable=clickable
		self.__fontSize=fontSize
		self.__style={'normal':None,'hover':None,'press':None,'active':None}
		self.Set_Style(style,styleHover,stylePress,styleActive,True)
		self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		self.Set_Clickable(clickable)
	@classmethod
	def Set_NewStyle(self,name:str,qss:str,clear:bool=False):
		'''
			注册新的样式表，qss可以是路径。
			name不可指定“Base”名称。
			clear为真时将无视name和qss，重置样式表数据

			特别的，该函数调用后不会立即生效，需对实际控件调用update刷新效果

			qss的值形如：
				“
					background: rgba(0, 127, 255, 12%);
					color: rgba(64, 127, 255, 87%);
					border-color: rgba(0, 128, 255, 75%);
					...
				”
		'''
		sm=self.__qssManager
		if(clear):
			sm.setStyleSheet('',clear=True)
			return sm.setStyleSheet(qss=GetRealPath('./styleSheet.qss'),multi=True)
		else:
			if(not name or name=='Base'):
				return False
			return sm.setStyleSheet(qss,name)
	@classmethod
	def Get_AvailableStyle(self):
		'''
			获取可用的样式表名称
		'''
		return self.__qssManager.styleSheet(returnNames=True)
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
	def Set_FontSize(self,fontSize:int):
		'''
			设置字体大小
		'''
		self.__fontSize=fontSize
		self.__SetStyleSheet()
	def Set_Style(self,
			   style:str,
			   styleHover:str=None,
			   stylePress:str=None,
			   styleActive:str=None,
			   series:bool=False):
		'''
			设置样式，
			如果指定series=True那么在指定style而其余三个样式有缺省的情况下会尝试使用配套样式，
			例如指定style='User'，那么其余样式会默认指定User系列，即'UserHover'、'UserPress'、'UserActive'。

			如果样式不存在则会暂时使用Gray系列(直到通过Set_NewStyleSheet设置新样式并调用update更新状态
		'''
		styleMap={'Normal':style,'Hover':styleHover,'Press':stylePress,'Active':styleActive}
		if(series):
			styleNormal=style
			for key,style in styleMap.items():
				if(not style):
					style=styleNormal+key
				self.__style[key.lower()]=style
		self.__SetStyleSheet()
	def Get_Active(self):
		'''
			返回当前状态
		'''
		return self.__active
	def Get_Clickable(self):
		'''
			返回可否点击
		'''
		return self.__clickable
	def update(self,*args):
		self.__SetStyleSheet()
		super().update(*args)
	def mousePressEvent(self,event):
		if(self.__clickable):
			super().mousePressEvent(event)
			self.Set_Active(not self.__active)
			self.clicked.emit(self.__active)
	def __GetStyleSheet(self,key:str='',default:str=''):
		key=self.__style.get(key,default)
		qss=self.__qssManager.styleSheet(key)
		if(not qss):
			qss=self.__qssManager.styleSheet(default)
		return qss
	def __SetStyleSheet(self):
		default='Gray'
		styleB=self.__GetStyleSheet(default='Base')
		styleN=self.__GetStyleSheet('normal',default)
		styleP=''
		styleH=''
		fontSize=f'font-size:{self.__fontSize}px;'
		if(self.__clickable):
			if(self.__active):
				styleN=self.__GetStyleSheet('active',default)
			styleH=self.__GetStyleSheet('hover',default)
			styleP=self.__GetStyleSheet('press',default)
		style=f'''
			.XJQ_Tag{{
				{styleB}
				{styleN}
				{fontSize}
			}}
			.XJQ_Tag:hover{{
				{styleH}
			}}
			.XJQ_Tag:pressed{{
				{styleP}
			}}
		'''
		self.setStyleSheet(style)







