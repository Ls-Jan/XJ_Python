
__version__='1.0.0'
__author__='Ls_Jan'

# from .XJQ_ListWidgetItem import *

from PyQt5.QtWidgets import QListWidget,QListWidgetItem,QWidget

__all__=['XJQ_ListWidget']

#TODO:【半成品】列表
class XJQ_ListWidget(QListWidget):#【半成品】列表
	'''
		半成品，可以塞控件的列表，但只建议塞XJQ_ListWidgetItem(因为单元格高度问题带来了不少麻烦)，
		本质上是继承QListWidget并仅仅简单封装几个行为罢了

		单行选中，屏蔽拖拽操作，主要作为导航栏使用
	'''
	changed=None#这个是信号，当需要显示其他页的数据时将会发出该信号，参数为start,count，分别对应起始索引和数据个数

	#隐藏单元格虚线：https://blog.csdn.net/can3981132/article/details/115320235
	#滚动条样式设置：https://blog.csdn.net/qq_39827640/article/details/127853530
	#(或许有用的参考)：https://blog.csdn.net/qq_36780295/article/details/110231541
	__style='''
			QListWidget{
				background:#222222;
				outline:none;
			}

			QListWidget::item{
				height:65px;
			}
			QListWidget::item:focus{
				background:transparent;
			}
			QListWidget::item:hover{
				background:rgba(255,255,255,48);
			}
			QListWidget::item:selected{
				background:rgba(255,255,255,32);
			}


			QScrollBar
			{
				background: rgba(255,255,255,5%);
				width: 6px;
			}
			QScrollBar::add-line {
				width:0;
				height:0;
			}
			QScrollBar::sub-line {
				width:0;
				height:0;
			}
			QScrollBar::handle {
				background: rgba(64,64,64,75%);
			}
			QScrollBar::sub-page {
				background: rgba(0,0,0,30%);
			}
			QScrollBar::add-page {
				background: rgba(0,0,0,30%);
			}
		'''
	def __init__(self):
		super().__init__()
		self.setStyleSheet(self.__style)
		self.resize(400,600)
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

