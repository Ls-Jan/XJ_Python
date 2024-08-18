from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QMouseEvent, QPainter
from PyQt5.QtWidgets import QStyle, QStyleOption, QWidget

#TODO：半成品
class Frame:
	'''
		记录三个UI数据，分别是：图标icon1、图标icon2和文本text；
		剩余数据用于服务文本text：字体font、颜色color、旋转量rotation(以90度为一个单位)、UI数据的排列方向
	'''
	icon1:QPixmap=None
	icon2:QPixmap=None
	text:str=None
	font:QFont=None
	color:QColor=None
	rotation:int=None
	def __init__(self,icon1:QPixmap=None,icon2:QPixmap=None,text:str=None,font:QFont=None,color:QColor=None,rotation:int=0):
		self.icon1=icon1
		self.icon2=icon2
		self.text=text
		self.font=font
		self.color=color
		self.rotation=rotation
	def copy(self):
		frame=self.__class__()
		frame.icon1=self.icon1
		frame.icon2=self.icon2
		frame.text=self.text
		frame.font=self.font
		frame.color=self.color
		frame.rotation=self.rotation
		return frame

class Status:
	'''
		记录按钮的四个状态(为Frame对象)，分别是默认、悬浮、点击和禁用。
		normal状态不建议为空。
	'''
	normal:Frame=None
	hover:Frame=None
	press:Frame=None
	disable:Frame=None
	def __init__(self,normal:Frame,hover:Frame=None,press:Frame=None,disable:Frame=None):
		self.normal=normal if normal else Frame()
		self.hover=hover if hover else Frame()
		self.press=press if press else Frame()
		self.disable=disable if disable else Frame()

__all__=['XJQ_SwitchButton']

class XJQ_SwitchButton(QLabel):
	'''
		复杂的切换型按钮，每次点击都会进入到下一状态并触发clicked(int)信号；
		按钮状态数建议控制在1~3，过多的状态会影响使用体验。

		本控件可作为QPushButton和QCheckBox的平替(倒不如说本身就是为了替代这些孱弱的控件才进行的开发)
	'''
	clicked=pyqtSignal(int)
	Status=Status
	Frame=Frame
	__statusLst:list
	__currStatus:Status
	__currFrame:Frame
	__currIndex:int
	__direction:QBoxLayout.Direction
	__alignment:Qt.AlignmentFlag
	__padding:int
	__offset:tuple
	def __init__(
			self,
			direction:QBoxLayout.Direction=QBoxLayout.Direction.LeftToRight,
			# alignment:Qt.AlignmentFlag=Qt.AlignVCenter,
			alignment:Qt.AlignmentFlag=Qt.AlignCenter):
		'''
			direction控制绘制元素的排列方向；
			alignment控制绘制的对齐位置；
		'''
		super().__init__()
		self.__statusLst=[]
		self.__currIndex=-1
		self.__currFrame=Frame()
		self.__currStatus=Status(None)
		self.__direction=direction
		self.__alignment=alignment
		self.__padding=4
		self.__offset=(48,48)
	def Opt_InsertStatus(self,status:Status,index:int=-1):
		'''
			插入一个状态
		'''
		if(index<0):
			index=len(self.__statusLst)
		self.__statusLst.insert(index,status)
		if(index<self.__currIndex or self.__currIndex<0):
			self.__currIndex+=1
	def Opt_RemoveStatus(self,index:int):
		'''
			移除一个状态
		'''
		if(0<=index<len(self.__statusLst)):
			self.__statusLst.pop(index)
			if(self.__currIndex>=index):
				self.__currIndex-=1
	def Get_CurrentIndex(self):
		'''
			设置当前状态索引值(-1是无效值)
		'''
		return self.__currIndex
	def Get_StatusCount(self):
		'''
			获取当前状态数
		'''
		return len(self.__statusLst)
	def Set_CurrentIndex(self,index:int):
		'''
			设置当前状态索引值
		'''
		if(index<0):
			index=0
		self.__currIndex=index
		if(0<=self.__currIndex<len(self.__statusLst)):
			self.__currStatus=self.__statusLst[self.__currIndex]
			self.__UpdateCurrFrame(self.__currStatus.normal,True)
			if(self.underMouse()):
				self.__UpdateCurrFrame(self.__currStatus.hover)
	def __UpdateCurrFrame(self,frame:Frame,focus:bool=False):
		'''
			根据传入的frame更新self.__currFrame
		'''
		if(focus):
			self.__currFrame=frame.copy()
		else:
			currFrame=self.__currFrame
			if(frame.icon1):
				currFrame.icon1=frame.icon1
			if(frame.icon2):
				currFrame.icon2=frame.icon2
			if(frame.text):
				currFrame.text=frame.text
			if(frame.font):
				currFrame.font=frame.font
			if(frame.color):
				currFrame.color=frame.color
			if(frame.rotation):
				currFrame.rotation=frame.rotation
		self.update()

	def mousePressEvent(self,event:QMouseEvent) -> None:
		self.__UpdateCurrFrame(self.__currStatus.press)
		self.update()
	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		if(event.button()==Qt.MouseButton.LeftButton):
			count=len(self.__statusLst)
			self.Set_CurrentIndex((self.__currIndex+1)%count if count else -1)
			self.clicked.emit(self.__currIndex)
			self.update()
	def enterEvent(self,event:QEnterEvent):
		self.__UpdateCurrFrame(self.__currStatus.hover)
		self.update()
	def leaveEvent(self,event:QEvent):
		self.__UpdateCurrFrame(self.__currStatus.normal)
		self.update()
	def paintEvent(self,event:QPaintEvent):
		def DrawIcon(ptr:QPainter,icon:QPixmap,frame:Frame,offset:tuple,reutrnSize:bool=False):
			size=QSize(0,0)
			if(icon):
				ptr.save()
				if(offset):
					ptr.translate(*offset)
				if(reutrnSize):
					size=icon.size()
				else:
					ptr.drawPixmap(0,0,icon)
				ptr.restore()
			return size if reutrnSize else None
		def DrawText(ptr:QPainter,text:str,frame:Frame,offset:tuple,reutrnSize:bool=False):
			size=QSize(0,0)
			if(text):
				ptr.save()
				if(offset):
					ptr.translate(*offset)
					# frame.rotation//90
				if(frame.font):
					ptr.setFont(frame.font)
				if(frame.color):
					ptr.setPen(frame.color)
				if(frame.rotation):
					ptr.rotate(frame.rotation)
				if(reutrnSize):
					size=ptr.fontMetrics().boundingRect(0,0,0,0,Qt.TextDontClip,frame.text).size()
					if(frame.rotation and frame.rotation%180):
						size.transpose()
				else:
					ptr.drawText(0,0,0,0,Qt.TextDontClip,text)
				ptr.restore()
			return size if reutrnSize else None

		if(0<=self.__currIndex<len(self.__statusLst)):
			ptr=QPainter(self)
			frame=self.__currFrame
			reverse=self.__direction==QBoxLayout.Direction.RightToLeft or self.__direction==QBoxLayout.Direction.BottomToTop
			horizontal=self.__direction==QBoxLayout.Direction.LeftToRight or self.__direction==QBoxLayout.Direction.RightToLeft
			size1=DrawIcon(ptr,frame.icon1,frame,None,True)
			size2=DrawIcon(ptr,frame.icon2,frame,None,True)
			sizeT=DrawText(ptr,frame.text,frame,None,True)
			w1,w2,wT=size1.width(),size2.width(),sizeT.width()
			h1,h2,hT=size1.height(),size2.height(),sizeT.height()
			sW=sum((w1,w2,wT))
			sH=sum((h1,h2,hT))
			mW=max(w1,w2,wT)
			mH=max(h1,h2,hT)
			bW=sW if horizontal else mW
			bH=mH if horizontal else sH

			W=self.width()
			H=self.height()
			offsetLst=[[],[],[]]
			order=[tuple(reversed(item)) if reverse else item for item in ((w1,w2,wT),(h1,h2,hT),(frame.icon1,frame.icon2,frame.text),(DrawIcon,DrawIcon,DrawText))]
			for item in [
				[(Qt.AlignmentFlag.AlignLeft,Qt.AlignmentFlag.AlignHCenter,Qt.AlignmentFlag.AlignRight,self.__alignment),W,bW,order[0],horizontal],
				[(Qt.AlignmentFlag.AlignTop,Qt.AlignmentFlag.AlignVCenter,Qt.AlignmentFlag.AlignBottom,self.__alignment),H,bH,order[1],not horizontal],]:
				for i in range(4):
					if(self.__alignment&item[0][i]):
						diff=i%3/2*(item[1]-item[2])
						if(item[4]):
							offsetLst[0].append(diff)
							for j in range(2):
								offsetLst[j+1].append(offsetLst[j][-1]+item[3][j])
						else:
							for j in range(3):
								offsetLst[j].append(diff+1/2*(item[2]-item[3][j]))
						break
				# print("???",i)
			# print()
			# print(offsetLst)
			print(bW,bH,size1,size2,sizeT)
			# print(order[1:-2])
			ptr.translate(*self.__offset)
			for i in range(3):
				data=order[2][i]
				func=order[3][i]
				func(ptr,data,frame,offsetLst[i])




if True:
	app=QApplication([])

	lb=XJQ_SwitchButton()
	# lb=XJQ_SwitchButton(alignment=Qt.AlignLeft|Qt.AlignTop)
	# lb.Opt_InsertStatus(Status(Frame(None,None,"AAA"),Frame(text="BBB"),Frame(text="CCC"),Frame(text="DDD")))
	# lb.Opt_InsertStatus(Status(Frame(QPixmap('AAA.png').scaled(64,64),None,"Normal-A\n???",rotation=270),Frame(text="Hover-A"),Frame(text="Press-A"),Frame(text="DDD")))
	# lb.Opt_InsertStatus(Status(Frame(QPixmap('AAA.png').scaled(64,64),QPixmap('BBB.png').scaled(64,64),"Normal-A\n???"),Frame(text="Hover-A"),Frame(text="Press-A"),Frame(text="DDD")))
	# lb.Opt_InsertStatus(Status(Frame(QPixmap('AAA.png').scaled(64,64),QPixmap('BBB.png').scaled(64,64),"Normal-A\n???",rotation=1),Frame(text="Hover-A"),Frame(text="Press-A"),Frame(text="DDD")))
	# lb.Opt_InsertStatus(Status(Frame(QPixmap('AAA.png').scaled(64,64),QPixmap('BBB.png').scaled(64,64),"Normal-A\n???",rotation=2),Frame(text="Hover-A"),Frame(text="Press-A"),Frame(text="DDD")))
	lb.Opt_InsertStatus(Status(Frame(QPixmap('AAA.png').scaled(64,64),QPixmap('BBB.png').scaled(64,64),"Normal-A\n???",rotation=3),Frame(text="Hover-A"),Frame(text="Press-A"),Frame(text="DDD")))
	# lb.Opt_InsertStatus(Status(Frame(QPixmap('AAA.png').scaled(64,64),None,"Normal-A\n???"),Frame(text="Hover-A"),Frame(text="Press-A"),Frame(text="DDD")))
	# lb.Opt_InsertStatus(Status(Frame(QPixmap('BBB.png').scaled(32,32),None,"BBBN"),Frame(text="BBBH"),Frame(text="BBBP"),Frame(text="ddd")))
	lb.Opt_InsertStatus(Status(Frame(text="Normal-C"),Frame(text="Hover-C"),Frame(text="Press-C"),Frame(text="ddd")))
	lb.Set_CurrentIndex(0)
	lb.show()
	lb.resize(500,400)

	exit(app.exec())

