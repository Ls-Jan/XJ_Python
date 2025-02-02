
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_ScreenAreaSelector']

from PyQt5.QtGui import QPainter,QPen,QColor,QPixmap
from PyQt5.QtCore import Qt,QRect,QPoint,pyqtSignal
from PyQt5.QtWidgets import QWidget

from ...Structs.XJ_RectResize import XJ_RectResize
from ...Functions.Screenshot import Screenshot
from ...Functions.GetScreensArea import GetScreensArea

class XJQ_ScreenAreaSelector(QWidget):
	'''
		屏幕选区器，可用于截图或是显式指定某块区域。
		左键双击会发送selected信号(如果设置了QulckSelect则鼠标抬起即发送)，
		右键清除选区，再次右键将隐藏工具
	'''
	selected=pyqtSignal()
	def __init__(self):
		super().__init__()
		self.setStyleSheet('background:#444444')
		self.__rs=XJ_RectResize()
		self.__rs.Set_BorderThickness(20)
		self.__dragCorner=False#当拖拽角点时需要变化光标
		self.__freeze=True
		self.__fixed=False
		self.__qulckSelect=False
		self.__screenshot=None#临时截图(QPixmap)
		self.__drawCache=QPixmap()#缓存，避免频繁创建QPixmap对象
		self.__borderThickness=5
		self.__color=[#颜色分别是：外、边界、内
			[QColor(0,0,0,64),QColor(255,0,255),QColor(0,255,255,128)],#浮动，可拖拽
			[QColor(0,0,0,32),QColor(255,0,255),QColor(0,255,255,128)],#固定，点击穿透
		]
		self.setMouseTracking(True)
		self.resize(1200,700)
		# winFlags=Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint|Qt.ToolTip#窗口置顶+窗体无边界+去除任务栏图标
		winFlags=Qt.FramelessWindowHint|Qt.ToolTip#窗体无边界+去除任务栏图标
		self.setWindowFlags(winFlags)
	def Set_Color(self,outer:QColor=None,border:QColor=None,inner:QColor=None,fixed:bool=False):
		'''
			设置颜色。
			fixed决定颜色设置要作用于哪个模式
		'''
		index=1 if fixed else 0
		lst=[outer,border,inner]
		for i in range(3):
			if(lst[i]!=None):
				self.__color[index][i]=lst[i]
	def resizeEvent(self,event):
		self.__drawCache=QPixmap(self.size())
		self.__rs.Set_LimitArea(0,0,self.width(),self.height())
		self.__Opt_UpdateCache()
	def paintEvent(self,event):
		ptr=QPainter(self)
		if(self.__screenshot):
			ptr.drawPixmap(0,0,self.__screenshot)
		ptr.drawPixmap(0,0,self.__drawCache)
	def showEvent(self,event):
		self.__drawCache=QPixmap(self.size())
		area=GetScreensArea(joint=True)
		pix=Screenshot(area)
		self.setGeometry(area)
		self.__rs.Set_LimitArea(0,0,self.width(),self.height())
		self.__screenshot=pix if self.__freeze else None
		self.__Opt_UpdateCache()
		self.setCursor(Qt.CursorShape.ArrowCursor)
		self.update()
	def __Opt_UpdateCache(self):
		index=1 if self.__fixed else 0
		self.__drawCache.fill(self.__color[index][0])
		LTRB=self.__rs.Get_Rect()
		if(LTRB):
			area=QRect(QPoint(*LTRB[:2]),QPoint(*LTRB[2:]))
			ptr=QPainter(self.__drawCache)
			ptr.setPen(QPen(self.__color[index][1],self.__borderThickness))
			ptr.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
			ptr.fillRect(area,self.__color[index][2])
			ptr.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
			ptr.fillRect(area,self.__color[index][2])
			ptr.drawRect(area)
			ptr.end()
	def mouseMoveEvent(self,event):
		self.__rs.Opt_Move(event.pos().x(),event.pos().y())
		self.update()
		anchor=self.__rs.Get_HoverPos()
		if(self.__rs.Get_IsPressed()):#拖拽
			if(self.__dragCorner):#拖拽角点时行为比较特殊，其余时候不变
				if(anchor in {1,9}):#左上+右下
					self.setCursor(Qt.CursorShape.SizeFDiagCursor)
				elif(anchor in {3,7}):#右上+左下
					self.setCursor(Qt.CursorShape.SizeBDiagCursor)
			self.__Opt_UpdateCache()
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
				if(self.__rs.Get_Rect()==None):#无矩形，十字光标
					self.setCursor(Qt.CursorShape.SizeAllCursor)
				else:
					self.setCursor(Qt.CursorShape.ArrowCursor)
	def mousePressEvent(self,event):
		if(event.button()==Qt.MouseButton.LeftButton):
			self.__rs.Opt_Press()
			anchor=self.__rs.Get_HoverPos()
			self.__dragCorner=anchor in {1,3,7,9}#判断是否拖拽角点
		elif(event.button()==Qt.MouseButton.RightButton):
			if(self.__rs.Get_Rect()):
				self.Opt_Clear()
				self.update()
			else:
				self.hide()
	def mouseDoubleClickEvent(self,event):
		self.__rs.Opt_Move(event.pos().x(),event.pos().y())
		anchor=self.__rs.Get_HoverPos()
		if(anchor!=0 and event.button()==Qt.MouseButton.LeftButton):#左键双击矩形
			self.selected.emit()
		else:
			self.mousePressEvent(event)
	def mouseReleaseEvent(self,event):
		if(self.__qulckSelect and event.button()==Qt.MouseButton.LeftButton):#快速选择时左键抬起即触发selected信号
			self.selected.emit()
		self.__rs.Opt_Release()
		self.__Opt_UpdateCache()
		self.update()
	def Set_BorderThickness(self,thickness:int,extraDetectThickness:int=8):
		'''
			设置边界厚度。
			extraDetectThickness用于增加额外的探测宽度，以便鼠标距离边界一段距离也能进行拖拽
		'''
		self.__borderThickness=thickness
		self.__rs.Set_BorderThickness(thickness+extraDetectThickness*2)
	def Set_ScreenFreeze(self,flag:bool):
		'''
			是否冻结当前画面
		'''
		self.__freeze=flag
		area=GetScreensArea(joint=True)
		pix=Screenshot(area)
		self.__screenshot=pix if self.__freeze else None
		self.update()
	def Set_Fixed(self,flag:bool):
		'''
			是否固定。固定后无法选中(即鼠标事件穿透)
		'''
		self.__fixed=flag
		self.setAttribute(Qt.WA_TransparentForMouseEvents,flag)#鼠标事件穿透
	def Opt_Clear(self):
		'''
			清除选中区域
		'''
		self.__rs.Opt_ClearRect()
	def Set_Area(self,L:int,T:int,R:int,B:int):
		'''
			设置选中区域
		'''
		self.__rs.Set_Rect(L,T,R,B)
	def Get_Screenshot(self):
		'''
			获取截图，如果没有截取区域则返回None
		'''
		LTRB=self.__rs.Get_Rect()
		pix=None
		if(LTRB):
			area=QRect(QPoint(*LTRB[:2]),QPoint(*LTRB[2:]))
			if(self.__screenshot!=None):
				pix=self.__screenshot.copy(area)
			else:
				pix=Screenshot(area)
		return pix
	def Set_QuickSelect(self,flag:bool):
		'''
			快速选择，如果该值为真，在鼠标释放时即刻发出selected信号而无需双击
		'''
		self.__qulckSelect=flag
	@staticmethod
	def Opt_CreateCaptureButton(self,btnPict:QPixmap):
		'''
			生成一个XJQ_ScreenCapture以及一个QPushButton，
			点击按钮即截图
		'''

