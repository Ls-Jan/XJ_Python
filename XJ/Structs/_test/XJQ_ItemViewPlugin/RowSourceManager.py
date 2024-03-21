
from ...XJQ_ItemViewPlugin.RowSourceManager import *

from PyQt5.QtWidgets import QAbstractItemView,QApplication,QListView
from PyQt5.QtGui import QStandardItemModel,QStandardItem


if True:
	app=QApplication([])

	lv=QListView()
	model=QStandardItemModel()
	lv.setModel(model)
	for i in range(200):
		model.appendRow(QStandardItem(str(i)))
	lv.setSelectionMode(QAbstractItemView.ExtendedSelection)
	lv.setEditTriggers(QAbstractItemView.NoEditTriggers)
	lv.show()

	lp=RowSourceManager(lv)
	lp.rowShowChanged.connect(lambda indices,show:print('\n',sorted(indices)) if show else print(">>>",sorted(indices)))
	lp.Set_RollTime(0.3)
	lp.Set_RetentionTime(1)
	lp.Set_DelayTime(0)
	lp.Set_RowExtend(0)
	
	app.exec()

