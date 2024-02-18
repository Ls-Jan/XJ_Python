from ..XJQ_ListWidget import *
from ..XJQ_ListWidgetItem import *

import sys
from PyQt5.QtWidgets import QApplication

if True:
	app = QApplication(sys.argv)

	lst=[
		('测试',['标签1','标签2'],'rgba(255,160,0,128)'),
		('测试',['标签1','标签2'],'rgba(255,0,0,128)'),
		('测试',['标签1','标签2'],'rgba(0,0,255,128)'),
		('测试',['标签1','标签2'],'rgba(255,160,0,128)'),
		('测试',['标签1','标签2'],'rgba(0,0,255,128)'),
		]

	lv=XJQ_ListWidget()
	lv.show()
	lst=[XJQ_ListWidgetItem(*lst[i%5]) for i in range(16)]
	for wid in lst:
		lv.Opt_AppendWidget(wid)
	# lv.Opt_RemoveRow(0)
	# lv.Opt_Clear()
	lv.currentRowChanged.connect(lambda item:print(item))

	sys.exit(app.exec_())

