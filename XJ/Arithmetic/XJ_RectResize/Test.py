__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJ_RectResize import XJ_RectResize

from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QRect,QPoint,Qt
from PyQt5.QtGui import QPen,QPainter

# TODO：样例未完成
class Win(QFrame):
	def __init__(self):
		super().__init__()
		self.setStyleSheet('background:#444444')
		self.__rs=XJ_RectResize()
		# self.__rs.Set_BorderThickness(5)
		self.__rs.Set_BorderThickness(10)
		self.__rs.Set_LimitArea(100,100,1000,650)
		# self.__rs.Set_LimitSize((100,100))
		# self.__rs.Set_LimitSize((100,100),(300,300))
		# self.__rs.Set_SizeRate(5,6)
		self.__rs.Set_SizeRate(1,2)
		self.__rs.Set_SmoothResize(True)
		# self.__rs.Set_Flippable(True,True)
		self.__rs.Set_Rect(400,100,700,200)
		self.__dragCorner=False#当拖拽角点时需要变化光标
		# self.__rs.Set_LimitSize(200,600,100,300)
		# self.__rs.Set_OnlyPoint(True)
		# self.__rs.Set_Flippable(False,False)
		self.setMouseTracking(True)
		self.resize(1200,700)
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
	def mousePressEvent(self,event):
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


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=Win()
		self.__win=win
	def Opt_Run(self):
		self.__win.show()
		super().Opt_Run()
		return self.__win






