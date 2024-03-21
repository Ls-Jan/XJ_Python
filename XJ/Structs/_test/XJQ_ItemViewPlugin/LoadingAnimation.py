
from ....Functions.GetRealPath import *
from ...XJQ_ItemViewPlugin.LoadingAnimation import *

from PyQt5.QtWidgets import QApplication,QListView
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QIcon
from PyQt5.QtCore import Qt,QSize

if True:
	app=QApplication([])

	lvModel=QStandardItemModel()
	lv=QListView()
	lv.setModel(lvModel)
	lv.setIconSize(QSize(128,128))
	lv.show()
	lv.resize(400,600)
	for i in range(200):
		item=QStandardItem(str(i))
		item.setCheckable(True)
		item.setEditable(False)
		item.setCheckState(Qt.CheckState.Checked)
		lvModel.insertRow(i,item)

	iconPath=GetRealPath('../../Icons/加载动画-1.gif')
	
	loadingRole=Qt.UserRole+16
	for i in range(0,10):
		item=lvModel.item(i)
		item.setIcon(QIcon(QIcon(GetRealPath('../../Icons/加载动画-6.gif')).pixmap(QSize(64,64)).scaled(32,32)))
		# item.setIcon(QIcon(GetRealPath('../../Icons/加载动画-6.gif')))
		# item.setIcon(QIcon(GetRealPath('../../Icons/保存.png')))
	for i in range(0,150,2):
		item=lvModel.item(i)
		item.setData(True,loadingRole)
	kkk=LoadingAnimation(iconPath,view=lv,loadingRole=loadingRole)
	app.exec()
