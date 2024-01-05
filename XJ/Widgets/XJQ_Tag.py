from enum import Enum
from PyQt5.QtWidgets import QLabel

__all__=['XJQ_Tag']
class XJQ_Tag(QLabel):
	class Style(Enum):#别问，问就是一点一点试的。我也想扒样式表但不知道哪里才有。
		#颜色取值参考了Element-plus的按钮样式：https://element-plus.org/zh-CN/component/button.html
		Base='''
			border-width:2px;
			border-style:solid;
			border-radius: 10px;
			font-size:25px;
			padding:1px 2px;
			width:fit-content;
			height:fit-content;
			'''
		Blue='''
			background:rgba(0,127,255,32);
			color:rgba(64,127,255,224);
			border-color:rgba(0,128,255,192);
			'''
		Red='''
			background:rgba(255,0,0,32);
			color:rgba(255,64,64,224);
			border-color:rgba(255,32,32,192);
			'''
		Green='''
			background:rgba(0,255,0,32);
			color:rgba(64,255,64,224);
			border-color:rgba(32,255,32,192);
			'''
		Gray='''
			background:rgba(144,144,144,64);
			color:rgba(128,128,128,224);
			border-color:rgba(128,128,128,192);
			'''
		Orange='''
			background:rgba(255,156,0,48);
			color:rgba(255,156,0,224);
			border-color:rgba(255,192,128,192);
			'''
	def __init__(self,parent,text,style=Style.Blue,fontSize=25):
		super().__init__(parent)
		self.Set_Text(text)
		self.Set_Style(style,fontSize)
	def Set_Text(self,text):
		self.setText(text)
	def Set_Style(self,style,fontSize=25):
		style=self.Style.Base.value+style.value+f'font-size:{fontSize}px;'
		self.setStyleSheet(style)
