__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_InsertPreviewMask']

from PyQt5.QtWidgets import QWidget,QLayout,QApplication
from PyQt5.QtCore import Qt,QRect,QPoint
from PyQt5.QtGui import QPainter,QColor,QPixmap,QTransform,QCursor
from ....Structs.XJ_Section import XJ_Section

class XJQ_InsertPreviewMask(QWidget):
	'''
		用于数据插入的可视化。
		主用于布局内控件的插入，其他场合未实测。
		被依附的主控件在重写dragEnterEvent、dragMoveEvent、dropEvent时要去主动调用本类的show、update、hide函数。
	'''
	def __init__(self,parent:QWidget):
		super().__init__(parent)
		self.__r=30
		self.__validDire=[True,True]
		self.__wid=None
		self.__dire=0
		self.__arrowUp=None
		self.__col_default=QColor(0,0,0,64)
		self.__col_widget=QColor(255,0,0,64)
		self.__col_border=QColor(0,0,255,64)
		self.__excludeWids=set()
		self.__includeLayouts=set()
		self.__layoutAreas=[]#include中的布局的位置(已经映射到屏幕坐标)
		self.__drawArea=[QRect(),None]#依次是布局和控件的位置(已经映射到本控件上)
		self.setAttribute(Qt.WA_TransparentForMouseEvents, True)#鼠标事件穿透
		self.raise_()
	@staticmethod
	def __Opt_DrawArrow(pix:QPixmap,ptr:QPainter,rect:QRect,TLRB:int):
		'''
			提供上箭头图片pix，
			使用画笔ptr，
			在区域rect内，
			根据箭头方向TLRB旋转箭头并进行绘制，可取值为0123，对应'TLRB'的含义(即上左右下)
		'''
		if(pix):
			P=[pix.width(),pix.height()]
			LT=[rect.left(),rect.top()]
			WH=[rect.width(),rect.height()]
			for i in range(2):
				if(WH[i]<0):
					LT[i]+=WH[i]
					WH[i]=-WH[i]
			for i in range(2):
				if(P[i]>WH[i]):
					P[(i+1)%2]=int(P[(i+1)%2]*WH[i]/P[i])
					P[i]=WH[i]
					pix=pix.scaled(*P)
			P=[P[i]>>1 for i in range(2)]
			C=[LT[i]+(WH[i]>>1) for i in range(2)]
			trans=[
				QTransform(1,0,0,0,1,0,C[0]-P[0],LT[1],1),#上
				QTransform(0,1,0,1,0,0,LT[0],C[1]-P[1],1),#左
				QTransform(0,1,0,-1,0,0,LT[0]+WH[0],C[1]-P[1],1),#右
				QTransform(1,0,0,0,-1,0,C[0]-P[0],LT[1]+WH[1],1),#下
			]
			ptr.save()
			ptr.setTransform(trans[TLRB%4])
			ptr.drawPixmap(0,0,pix)
			ptr.restore()
	def Set_Color(self,default:QColor=None,widget:QColor=None,border:QColor=None):
		'''
			设置颜色，分别是蒙版颜色、控件颜色以及控件边缘插入颜色
		'''
		if(default):
			self.__col_default=default
		if(widget):
			self.__col_widget=widget
		if(border):
			self.__col_border=border
	def Set_UpArrowPict(self,arrow:QPixmap):
		'''
			设置箭头图标，可为None(不绘制)
		'''
		self.__arrowUp=arrow
	def Set_ExcludeWidgets(self,*wids:QWidget):
		'''
			设置排除在外的控件，这些控件所在区域将不被被阴影遮盖
		'''
		self.__excludeWids=set(wids)
	def Set_IncludeLayout(self,*layouts:QLayout):
		'''
			设置包含在内的布局，这些布局所在区域将被阴影遮盖
		'''
		self.__includeLayouts=set(layouts)
	def Set_DetectRadius(self,r:int):
		'''
			设置检测半径，以判断鼠标距离控件的哪个边缘比较近
		'''
		self.__r=r
	def Set_ValidDire(self,horizontal:bool,vertical:bool):
		'''
			设置有效的插入方向
		'''
		self.__validDire=[horizontal,vertical]
	def Get_InsertPos(self):
		'''
			获取插入点，返回的是控件以及方向值。

			方向值有5种可取，图示如下，就是一个十字：
				    2    
				4	5	6
					8
			5为中心，2为上，8为下，4为左，6为右
		'''
		return self.__wid,self.__dire
	def update(self):
		dire=0#该值仅在当前控件有效时不为0
		pos=QCursor.pos()
		wid=QApplication.widgetAt(pos)
		if(wid):
			layoutArea=None
			widArea=wid.geometry()
			widArea.moveTopLeft(wid.mapToGlobal(QPoint(0,0)))
			if(self.__layoutAreas and wid not in self.__excludeWids):
				if(self.__wid!=wid):#当前控件发生变化
					for layoutArea in self.__layoutAreas:
						if(layoutArea.contains(widArea)):#控件在目标布局内，确定dire
							dire=5
							break
				else:
					dire=5
		if(dire>0):#修改dire，该值只可能取2、4、6、8、5
			pos=wid.mapFromGlobal(pos)
			groups=((pos.x(),wid.width()),(pos.y(),wid.height()))
			for i in range(2):
				if(self.__validDire[i]):
					s=XJ_Section(0,groups[i][1])
					p=s.Get_ValuePos(groups[i][0],self.__r)#此时p值必然只会是1、2、3中的一个
					w=1|(1<<i)#取巧了，不管，能用就行
					if(p==1):
						dire-=w
					elif(p==3):
						dire+=w
			if(dire!=5 and dire%2==1):#奇数，对应1、3、7、9，即鼠标当前在角点位置，找个最近的边
				dw=pos.x()
				dh=pos.y()
				if(dire>5):#对应7和9(下)
					dh=wid.height()-pos.y()
				if(dire==3 or dire==9):#对应3和9(右)
					dw=wid.width()-pos.x()
				if(dh<dw):#靠近上下边
					dire=2<<((dire-1)//3)
				else:#靠近左右边
					dire=6-((dire%3)<<1)
		if(self.__wid!=wid or self.__dire!=dire):#任一发生变化
			self.__wid=wid
			self.__dire=dire
			if(dire>0):
				widArea.moveTopLeft(self.mapFromGlobal(widArea.topLeft()))
				if(layoutArea):
					layoutArea=QRect(layoutArea)
					layoutArea.moveTopLeft(self.mapFromGlobal(layoutArea.topLeft()))
					self.__drawArea[0]=layoutArea
				self.__drawArea[1]=widArea
			super().update()
	def showEvent(self,event):
		parent=self.parent()
		if(parent):
			self.resize(parent.size())
			self.__excludeWids.add(parent)
		self.__wid=None
		self.__drawArea[0]=QRect()
		self.__layoutAreas.clear()
		for layout in self.__includeLayouts:
			rect=layout.geometry()
			obj=layout
			while(obj):
				obj=obj.parent()
				if(isinstance(obj,QWidget)):
					pos=obj.mapToGlobal(rect.topLeft())
					rect.moveTopLeft(pos)
					self.__layoutAreas.append(rect)
		self.raise_()
		self.update()
	def paintEvent(self,event):
		pix=QPixmap(self.size())
		pix.fill(Qt.GlobalColor.transparent)
		ptr=QPainter(pix)
		ptr.fillRect(self.__drawArea[0],self.__col_default)
		if(self.__dire>0):
			dire=self.__dire
			if(dire>0):
				rect=self.__drawArea[1]
				ptr.fillRect(rect,Qt.GlobalColor.transparent)
				ptr.fillRect(rect,self.__col_widget)
				if(dire==2):
					rect.setBottom(rect.top()+self.__r)
				elif(dire==4):
					rect.setRight(rect.left()+self.__r)
				elif(dire==6):
					rect.setLeft(rect.right()-self.__r+1)
				elif(dire==8):
					rect.setTop(rect.bottom()-self.__r+1)
				else:
					dire=0
				if(dire):
					ptr.eraseRect(rect)
					ptr.fillRect(rect,self.__col_border)
					self.__Opt_DrawArrow(self.__arrowUp,ptr,rect,(dire>>1)-1)
		ptr.end()
		ptr=QPainter(self)
		ptr.drawPixmap(0,0,pix)



