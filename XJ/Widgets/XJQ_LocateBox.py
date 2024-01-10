

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize,Qt,QPoint,QRect


class XJQ_LocateBox(QWidget):#定位型容器
	'''
		定位型容器，或者称其为牛皮癣
		底层实现是通过paintEvent这个函数灵活获取父控件的大小，以计算并定位容器控件位置
		该方法也是有缺陷的，当窗口一口气缩小到看不见容器的话容器位置将无法得到响应，
		解决方法四种，这里采用最优解
			1.【极不建议】对父控件安装事件过滤installEventFilter(不建议做出破坏其他控件属性这种高耦合的行为)
			2.【极不建议】安装全局事件过滤(影响性能、增加耦合)
			3.【较优解】塞个定时器
			4.【最优解】控件大小始终保持和父控件一致，这样代码的核心就控制在paintEvent中，可喜可贺
	'''
	def __init__(self,
			parent,#父控件
			content=None,#容器元素
			align=Qt.AlignCenter,#定位，有九个位置
			margin=(0,0),#与边缘之间的留白，大于1的数以像素计算，小数则以(剩余空白)百分比计算
			):
		if(not parent):
			raise Exception('XJQ_LocateBox参数错误，请指定父控件')
		super().__init__(parent)
		if(not content):
			content=QWidget()
		content.setParent(parent)#这里不是设置到容器上面的原因是，鼠标穿透时会把容器元素也穿过去
		self.__content=content
		self.__align=align
		self.__margin=margin
		self.setAttribute(Qt.WA_TransparentForMouseEvents,True)#鼠标事件穿透
	def Get_Content(self):
		return self.__content
	def Set_Content(self,wid):
		self.__content.setParent(None)
		self.__content=wid
		wid.setParent(self.parent())
		self.update()
	def Set_Align(self,align):
		self.__align=align
		self.update()
	def Set_Margin(self,margin):
		self.__margin=margin
		self.update()
	def paintEvent(self,event):
		pSize=self.parent().size()
		if(self.size()==pSize):#规避无效的paintEvent
			return
		self.resize(pSize)
		cSize=self.__content.sizeHint()
		if(not cSize):
			cSize=self.size()
		dW=pSize.width()-cSize.width()
		dH=pSize.height()-cSize.height()
		lst=[
			(dW,(
				Qt.AlignLeft,
				Qt.AlignHCenter,
				Qt.AlignRight)),
			(dH,(
				Qt.AlignTop,
				Qt.AlignVCenter,
				Qt.AlignBottom))]
		for i in range(2):
			diff,align=lst[i]
			for j in range(3):
				if(int(self.__align&align[j])):
					margin=self.__margin[i]
					if(0<margin<1):
						margin=margin*diff
					if(j==1):
						margin=0
					elif(j>1):
						margin=-margin
					lst[i]=diff*j/2+margin
					break
				if(isinstance(lst[i],tuple)):
					lst[i]=diff/2
		self.__content.setGeometry(QRect(QPoint(*lst),cSize))


