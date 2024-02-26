from ..GetQItemViewShowingIndices import *

from PyQt5.QtWidgets import QApplication,QListView,QListWidget,QAbstractItemView,QTableView
from PyQt5.QtGui import QStandardItemModel,QStandardItem


if True:
	app=QApplication([])

	# view=QListView()
	# model=QStandardItemModel()
	# view.setModel(model)
	# for i in range(200):
	# 	model.appendRow(QStandardItem(str(i)))

	# view=QListWidget()
	# for i in reversed(range(200)):
	# 	view.insertItem(0,str(i))

	view=QTableView()
	model=QStandardItemModel()
	view.setModel(model)
	for i in range(200):
		model.setItem(i,0,QStandardItem(str(i)))
	

	view.setSelectionMode(QAbstractItemView.ExtendedSelection)
	view.setEditTriggers(QAbstractItemView.NoEditTriggers)
	view.pressed.connect(lambda:print(GetQItemViewShowingIndices(view,1)))
	# view.pressed.connect(lambda:print([i.row() for i in view.selectedIndexes()]))
	view.show()
	
	app.exec()

