
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_RectResize']
#TODO：2024/8/18

from XJ_RectResize import XJ_RectResize

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class XJ_CropperBox(QFrame):
	'''
		进行选区
	'''
	def __init__(self):
		super().__init__()
		self.setStyleSheet('background:#444444')
		self.__rs=XJ_RectResize()
		self.__rs.Set_BorderThickness(10)
		# self.__rs.Set_BorderThickness(5)
		# self.__rs.Set_BorderThickness(50)
		self.__rs.Set_LimitArea(100,100,1000,650)
		# self.__rs.Set_LimitSize((100,100))
		# self.__rs.Set_SizeRate(1,2)
		self.__rs.Set_Rect(400,100,700,200)
		# self.__rs.Set
		self.__dragCorner=False#当拖拽角点时需要变化光标
		# self.__rs.Set_LimitSize(200,600,100,300)
		# self.__rs.Set_OnlyPoint(True)
		# self.__rs.Set_Flippable(False,False)
		self.setMouseTracking(True)
	def paintEvent(self,event):
		LTRB=self.__rs.Get_Rect()
		if(LTRB):
			ptr=QPainter(self)
			pen=QPen()
			pen.setWidth(5)
			# pen.setWidth(50)
			ptr.setPen(pen)
			ptr.drawRect(QRect(QPoint(*LTRB[:2]),QPoint(*LTRB[2:])))
	def mouseMoveEvent(self,event):
		pos=event.pos()
		pos=(pos.x(),pos.y())
		self.__rs.Opt_Move(*pos)
		self.update()
		anchor=self.__rs.Get_HoverPos()
		if(self.__rs.Get_IsPressed()):#拖拽
			if(self.__dragCorner):#拖拽角点时行为比较特殊，其余时候不变
				if(anchor in {1,9}):#左上+右下
					self.setCursor(Qt.CursorShape.SizeFDiagCursor)
				elif(anchor in {3,7}):#右上+左下
					self.setCursor(Qt.CursorShape.SizeBDiagCursor)
		else:
			if(anchor in {1,9}):#左上+右下
				self.setCursor(Qt.CursorShape.SizeFDiagCursor)
			elif(anchor in {3,7}):#右上+左下
				self.setCursor(Qt.CursorShape.SizeBDiagCursor)
			elif(anchor in {4,6}):#左右
				self.setCursor(Qt.CursorShape.SizeHorCursor)
			elif(anchor in {2,8}):#上下
				self.setCursor(Qt.CursorShape.SizeVerCursor)
			elif(anchor==5):#中
				self.setCursor(Qt.CursorShape.SizeAllCursor)
			else:#外
				self.setCursor(Qt.CursorShape.ArrowCursor)
	def mousePressEvent(self,event:QMouseEvent):
		if(event.button()==Qt.MouseButton.LeftButton):
			self.__rs.Opt_Press()
			anchor=self.__rs.Get_HoverPos()
			self.__dragCorner=anchor in {1,3,7,9}#判断是否拖拽角点
		elif(event.button()==Qt.MouseButton.RightButton):
			self.__rs.Opt_ClearRect()
			self.update()
	def mouseReleaseEvent(self,event):
		self.__rs.Opt_Release()
		# print(self.__rs.Get_Rect())

if True:
	app = QApplication([])

	t=Test()
	t.show()
	t.resize(1200,700)

	app.exec_()


