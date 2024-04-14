
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt,QPoint,QRect

__all__=['XJQ_LocateBox']
class XJQ_LocateBox(QWidget):#定位型容器
	'''
		定位型容器，或者称其为牛皮癣。
		底层实现是通过paintEvent这个函数灵活获取父控件的大小，以计算并定位容器控件位置
	'''
	def __init__(self,parent:QWidget):#父控件
		if(not parent):
			raise Exception('XJQ_LocateBox参数错误，请指定父控件')
		super().__init__(parent)
		self.__widgets={}
		self.setAttribute(Qt.WA_TransparentForMouseEvents,True)#鼠标事件穿透
		self.update()
	def Opt_AddWidget(self,
			wid:QWidget=None,#容器元素
			align=Qt.AlignCenter,#定位，有九个位置
			margin:tuple=(0,0),):#与边缘之间的留白，大于1的数以像素计算，小数则以(剩余空白)百分比计算
		'''
			添加控件到本容器中。
			设置align以确定控件位置，9个位置可选；
			设置margin以调整控件与边界之间的空白，大于1的数以像素计算，小数则以(剩余空白)百分比计算
		'''
		self.__widgets[wid]=(align,margin)
		wid.setParent(self.parent())
		self.update()
	def Opt_RemoveWidget(self,wid:QWidget):
		'''
			移除指定控件
		'''
		if(wid in self.__widgets):
			wid.setParent(None)
			self.__widgets.pop(wid)
			self.update()
	def paintEvent(self,event):
		pSize=self.parent().size()
		if(self.size()==pSize):#规避无效的paintEvent
			return
		self.resize(pSize)
		for wid in self.__widgets:
			wAlign,wMargin=self.__widgets[wid]
			cSize=wid.sizeHint()
			if(cSize.width()<=0 or cSize.height()<=0):
				cSize=wid.size()
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
				diff,cmpAlign=lst[i]
				for j in range(3):
					if(int(wAlign&cmpAlign[j])):
						margin=wMargin[i]
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
			# print(wid,cSize,wid.sizeHint(),wid.size())
			wid.setGeometry(QRect(QPoint(*lst),cSize))


