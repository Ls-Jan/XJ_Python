
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtWidgets import QListWidget,QListWidgetItem,QWidget
from ...Structs.XJQ_StyleSheetManager import XJQ_StyleSheetManager
from ...Functions.GetRealPath import GetRealPath

__all__=['XJQ_ListWidget']

#TODO:【半成品】列表
class XJQ_ListWidget(QListWidget):#【半成品】列表
	'''
		半成品，可以塞控件的列表，但只建议塞XJQ_ListWidgetItem(因为单元格高度问题带来了不少麻烦)，
		本质上是继承QListWidget并仅仅简单封装几个行为罢了

		单行选中，屏蔽拖拽操作，主要作为导航栏使用
	'''
	# changed=None#这个是信号，当需要显示其他页的数据时将会发出该信号，参数为start,count，分别对应起始索引和数据个数

	def __init__(self):
		super().__init__()
		self.setStyleSheet(None)
		self.resize(400,600)
	def setStyleSheet(self,qss:str):
		'''
			设置样式表，qss可以为文件路径。
			如果qss为空则设置为默认样式
		'''
		if(not qss):
			qss=GetRealPath('./styleSheet.qss')
		sm=XJQ_StyleSheetManager()
		sm.setStyleSheet(qss)
		super().setStyleSheet(sm.styleSheet())
	def Opt_AppendWidget(self,wid:QWidget):
		'''
			添加控件
		'''
		#向QListWidget中插入控件：https://blog.csdn.net/fsfsfsdfsdfdr/article/details/84036584
		item=QListWidgetItem()
		self.addItem(item)
		self.setItemWidget(item,wid)
	def Opt_RemoveRow(self,row):
		'''
			移除指定行
		'''
		#删除item：https://blog.csdn.net/u011417605/article/details/50935696
		self.takeItem(row)
	def Opt_Clear(self):
		'''
			清空
		'''
		self.clear()
	def mouseMoveEvent(self,event):#屏蔽拖拽时当前行切换的疯狂行为
		pass

