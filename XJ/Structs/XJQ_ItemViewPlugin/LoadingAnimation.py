
__version__='1.0.1'
__author__='Ls_Jan'

from PIL import Image
from PyQt5.QtCore import QModelIndex,Qt,QTimer,QSize
from PyQt5.QtGui import QPainter,QIcon
from PyQt5.QtWidgets import QStyledItemDelegate,QStyleOptionViewItem,QApplication,QStyle,QAbstractItemView

__all__=['LoadingAnimation']
class LoadingAnimation(QStyledItemDelegate):
	'''
		用于实现列表/表格的单元格数据加载效果。
		通过QStandardItem.setData(False/True,loadingRole)来设置单元格的加载状态，
		其中loadingRole为初始化时指定的值，默认为Qt.UserRole+16
	'''
	__loadingRole=None
	__timer=None
	__icon=None
	__iconLst=None
	__iconIndex=None
	__views=None
	__iconSizeFixed=True
	def __init__(self,gifPath:str=None,*,view:QAbstractItemView=None,loadingRole:Qt.ItemDataRole=Qt.UserRole+16):
		'''
			gifPath为动图路径，初始化后可以通过Set_LoadingGIF函数再次指定别的加载动图。
			指定view那么会自动调用view.setItemDelegate设置绘制代理为本对象。
			loadingRole的值可用户指定(值的选定建议参考官方手册。

			1、本实现是通过覆盖单元格设置的图标icon实现加载动图效果，换句话说就是如果单元格本身就有图标的话会被替换为加载动图
			2、单元格加载状态不由本对象设置，需通过单元格对象的函数setData(False/True,loadingRole)来设置单元格的加载状态。
			3、列表/表格控件通过setItemDelegate、setItemDelegateForColumn、setItemDelegateForRow设置绘制代理为本对象
		'''
		super().__init__()
		self.__loadingRole=loadingRole
		timer=QTimer(self)
		timer.timeout.connect(self.__Update)
		if(view):
			view.setItemDelegate(self)
		self.__timer=timer
		self.__animation=True
		self.__iconLst=[]
		self.__views=set()
		self.__iconIndex=0
		self.Set_LoadingGIF(gifPath)
		QApplication.instance().aboutToQuit.connect(self.Opt_StopGIF)
	@property
	def loadingRole(self):
		'''
			获取初始化时传入的loadingRole值
		'''
		return self.__loadingRole
	def Opt_StopGIF(self):
		'''
			停止动画。
			该操作已经与QApplication对象的AboutToQuit信号关联，在程序退出时会自动调用。
		'''
		self.__animation=False
		self.__timer.stop()
	def Opt_StartGIF(self):
		'''
			与Opt_StopGIF相对应，启动动画
		'''
		self.__animation=True
		for view in self.__views:
			view.viewport().update()
	def Set_iconSizeFixed(self,flag:bool=True):
		'''
			【新增】
			用于强制控制每个单元格的图标大小(尤其行高，即使没设置图标的单元格也一样)，使整份表格的图标大小规范化。
			图标大小由表格的iconSize控制。
			该功能默认启用
		'''
		self.__iconSizeFixed=flag
	def Set_LoadingGIF(self,path:str=None,msec:int=None):
		'''
			设置加载动画以及动画刷新间隔(ms)
		'''
		if(path):
			im = Image.open(path)
			im.load()#调用该函数后info中的信息才会有效(这是试出来的)
			if(msec==None):
				msec=im.info.get('duration',0)
			self.__iconLst.clear()
			for i in range(im.n_frames):
				im.seek(i)#设置当前所在帧
				self.__iconLst.append(QIcon(im.convert("RGBA").toqpixmap()))#gif的第0帧是P模式(调色板)
			self.__iconIndex=0
			self.__icon=self.__iconLst[0]
		if(msec):
			self.__timer.setInterval(msec)
	def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
		option=QStyleOptionViewItem(option)
		wid=option.widget
		style=wid.style() if wid else QApplication.style()
		self.initStyleOption(option,index)
		stat=index.model().data(index,self.__loadingRole)#获取加载状态
		if(stat):
			self.__views.add(wid)
			if(not self.__timer.isActive() and self.__animation):
				self.__timer.start()
			if(self.__icon):
				option.icon=self.__icon
				option.features|=QStyleOptionViewItem.HasDecoration#该标志决定icon的绘制
		style.drawControl(QStyle.CE_ItemViewItem,option,painter,wid)
	def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
		option=QStyleOptionViewItem(option)
		self.initStyleOption(option,index)
		stat=index.model().data(index,self.__loadingRole)#获取加载状态
		wid=option.widget
		style=wid.style() if wid else QApplication.style()
		if(stat and self.__icon):
			option.features|=QStyleOptionViewItem.HasDecoration#该标志决定是否绘制icon
		if(self.__iconSizeFixed):
			option.features|=QStyleOptionViewItem.HasDecoration
			if(isinstance(wid,QAbstractItemView)):
				option.decorationSize=wid.iconSize()#图标大小限制
		return style.sizeFromContents(QStyle.ContentsType.CT_ItemViewItem,option,QSize(),wid)
	def __Update(self):
		'''
			刷新动画(下一帧)。
			该函数与计时器绑定，用于自动获取动图下一帧。
		'''
		icon=None
		if(self.__views):#仅在view不为空的情况下才考虑加载下一帧
			if(len(self.__iconLst)):
				index=self.__iconIndex+1
				if(index>=len(self.__iconLst)):
					index=0
				self.__iconIndex=index
				icon=self.__iconLst[index]
		if(icon==None):#由于种种原因不需要下一帧的情况下，直接关掉计时器
			self.__timer.stop()
		else:
			self.__icon=icon
			for view in self.__views:
				view.viewport().update()
			self.__views.clear()

