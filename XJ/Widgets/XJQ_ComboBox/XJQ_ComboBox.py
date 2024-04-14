
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtWidgets import QComboBox,QListView
from PyQt5.QtWidgets import QStyle,QStylePainter,QStyleOptionComboBox,QStyleOptionButton
from PyQt5.QtGui import QPalette,QPainter,QFontMetrics
from PyQt5.QtCore import Qt,pyqtSignal,QPoint

__all__=['XJQ_ComboBox']
class XJQ_ComboBox(QComboBox):
	'''
		QComboBox的简单优化，主要处理了一些样式上的问题，例如颜色、大小、文本居中
		内容发生变化时发送indexChanged(int,str)信号
		滚轮滚动可修改当前值(这是QComboBox自带的功能)，
		为了避免滚轮修改时频繁触发indexChanged信号，特地增加了一个延迟行为(时长可指定)
	'''
	indexChanged=pyqtSignal(int,str)#当前行修改时发送信号(带延迟)，依次是索引值和对应文本
	__timerId=None
	__delay=150#延迟发送
	__showArrow=True
	def __init__(self,*args):
		super().__init__(*args)
		self.setCursor(Qt.PointingHandCursor)
		#样式QComboBox QAbstractItemView{...}要调用QComboBox.setView后生效：https://blog.csdn.net/Larry_Yanan/article/details/123556429
		self.setView(QListView())
		self.setFocusPolicy(Qt.NoFocus)
		self.currentIndexChanged.connect(self.__indexChanged)
	def Opt_SetDelay(self,delay:int):
		'''
			设置延迟时长(ms)
		'''
		self.__delay=delay
	def Set_ShowArrow(self,flag:bool):
		'''
			箭头绘制可以通过styleSheet修正，也可以通过本函数设置
		'''
		self.__showArrow=flag
	def Set_List(self,lst:list):
		'''
			设置组合框下拉列表
		'''
		for i in range(len(lst),self.count()):
			self.removeItem(0)
		for i in range(self.count(),len(lst)):
			self.addItem('')
		i=0
		for tx in lst:
			self.setItemText(i,str(tx))
			i+=1
	def __indexChanged(self,index):
		self.__timerId=self.startTimer(self.__delay)
	def paintEvent(self,event):
		#组合框文字居中：https://blog.csdn.net/eiilpux17/article/details/109501871
		painter=QStylePainter(self)
		painter.setPen(self.palette().color(QPalette.Text))

		opt=QStyleOptionComboBox()
		self.initStyleOption(opt)
		if(self.__showArrow):
			painter.drawComplexControl(QStyle.CC_ComboBox, opt)
		if (self.currentIndex() < 0):
			opt.palette.setBrush(QPalette.ButtonText, opt.palette.brush(QPalette.ButtonText).color().lighter())
		painter.end()

		painter2 =QPainter(self)
		buttonOpt=QStyleOptionButton()
		buttonOpt.initFrom(self)
		editRect = self.style().subControlRect(QStyle.CC_ComboBox, opt, QStyle.SC_ComboBoxEditField, self)
		buttonOpt.rect = editRect
		buttonOpt.text = opt.currentText
		if(self.__showArrow):
			self.style().drawControl(QStyle.CE_PushButtonLabel, buttonOpt, painter2, self)
		else:
			buttonOpt.rect.setWidth(self.size().width())
			self.style().drawControl(QStyle.CE_PushButton, buttonOpt, painter2, self)
	def addItem(self,tx):
		#列表项居中：https://blog.csdn.net/chenxipu123/article/details/87804513
		super().addItem(tx)
		self.model().item(self.count()-1).setTextAlignment(Qt.AlignCenter)
	def timerEvent(self,event):
		timerId=event.timerId()
		if(self.__timerId==timerId):
			self.indexChanged.emit(self.currentIndex(),self.currentText())
		self.killTimer(timerId)

	def __adjustListWidth(self):
		ft=self.font()
		ft.setPixelSize(30)
		fm=QFontMetrics(ft)
		width=0
		for i in range(self.count()):
			width=max(width,fm.width(self.itemText(i)))
		self.view().parentWidget().setFixedWidth(width+20)
	def showPopup(self):
		self.__adjustListWidth()
		super().showPopup()
		fm=self.view().parentWidget()
		pt=fm.mapToGlobal(fm.pos())
		pt=fm.mapFromGlobal( QPoint(pt.x() - (fm.width() - self.width())/2, pt.y()))
		fm.move(pt)


