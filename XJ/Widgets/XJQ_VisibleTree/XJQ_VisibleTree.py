
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_VisibleTree']


from ..XJQ_Resizable.Canvas import Canvas
from ..XJQ_Resizable.Widgets.PushButton import PushButton
from ..XJQ_Resizable.Widgets.Label import Label
from .XJ_TreeDrawer_Base import XJ_TreeDrawer_Base

from PyQt5.QtCore import QRect,QPoint
from PyQt5.QtGui import QPixmap,QPainter,QColor

from typing import List,Tuple


class XJQ_VisibleTree(XJ_TreeDrawer_Base):
	'''
		可视树绘制器。
		绘制结果基于XJ.Widgets.XJQ_Resizable下的Canvas(画布)、PushButton(按钮)、Label(标签)
	'''
	def __init__(self):
		super().__init__()
		self.__canvas=Canvas()
		self.__lines=Label(self.__canvas)
		self.__nodes:List[PushButton]=[PushButton(self.__canvas)]#一个根节点
		self.__ptr=QPainter()
		self.__pix=QPixmap(1,1)
		self.__lineWidth=1
		self.__canvas.show()
		self.__canvas.resize(1200,700)
		self.__lines.setLGeometry(QRect(0,0,100,100))
		self.Set_LineWidth()
	def Set_LineWidth(self,width:int=3):
		'''
			设置线条粗细(默认3)
		'''
		self.__lineWidth=width
		self.Opt_Update()
	def Get_Canvas(self):
		'''
			返回画布控件
		'''
		return self.__canvas
	def Get_Node(self,nodeID:int):
		'''
			返回节点控件
		'''
		return self.__nodes[nodeID]
	def _DrawStart(self,w:int,h:int):
		pix=QPixmap(w,h)
		pix.fill(QColor(0,0,0,0))
		ptr=self.__ptr
		ptr.begin(pix)
		pen=ptr.pen()
		pen.setWidth(self.__lineWidth)
		ptr.setPen(pen)
		self.__pix=pix
		self.__lines.setLGeometry(QRect(0,0,w,h))
		self.__canvas.Opt_MoveCenterTo(QPoint(w>>1,h>>1))
	def _DrawEnd(self):
		self.__ptr.end()
		self.__lines.setPixmap(self.__pix)
		self.__canvas.Opt_Update()
	def _DrawLine(self,x1:int,y1:int,x2:int,y2:int,rgba:Tuple[int,int,int,int]):
		ptr=self.__ptr
		ptr.setBrush(QColor(*rgba))
		ptr.drawLine(x1,y1,x2,y2)
	def _DrawNode(self,x:int,y:int,w:int,h:int,nodeID:int):
		nodes=self.__nodes
		for i in range(len(nodes),nodeID+1):
			node=PushButton(self.__canvas)
			self.__nodes.append(node)
			node.show()
		node:PushButton=nodes[nodeID]
		node.setLGeometry(QRect(x,y,w,h))


