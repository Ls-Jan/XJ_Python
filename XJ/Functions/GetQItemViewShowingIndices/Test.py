__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .GetQItemViewShowingIndices import GetQItemViewShowingIndices

from PyQt5.QtWidgets import QApplication,QListView,QListWidget,QAbstractItemView,QTableView
from PyQt5.QtGui import QStandardItemModel,QStandardItem


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		view=QListWidget()
		for i in range(200):
			view.insertItem(len(view),str(i))

		# # view=QListView()
		# view=QTableView()
		# model=QStandardItemModel()
		# view.setModel(model)
		# for i in range(200):
		# 	model.setItem(i,0,QStandardItem(str(i)))
		
		view.setSelectionMode(QAbstractItemView.ExtendedSelection)
		view.setEditTriggers(QAbstractItemView.NoEditTriggers)
		view.pressed.connect(lambda:print(GetQItemViewShowingIndices(view,0)))
		# view.pressed.connect(lambda:print([i.row() for i in view.selectedIndexes()]))
		self.__view=view
	def Opt_Run(self):
		print("点击列表/表格查看当前显示的行")
		self.__view.resize(500,400)
		self.__view.show()
		super().Opt_Run()
		return self.__view


