from ..XJQ_ListWidget import XJQ_ListWidget
from ..XJQ_ListWidgetItem import XJQ_ListWidgetItem

import sys
from PyQt5.QtWidgets import QApplication

if True:
	app = QApplication(sys.argv)

	lst=[
		'rgba(255,160,0,128)',
		'rgba(255,0,0,128)',
		'rgba(0,0,255,128)',
		'rgba(255,160,0,128)',
		'rgba(0,0,255,128)',
	]

	lv=XJQ_ListWidget()
	lv.show()
	lst=[XJQ_ListWidgetItem(str(i),[f'标签{j}' for j in range(i%5+1)],lst[i%5]) for i in range(16)]
	for wid in lst:
		lv.Opt_AppendWidget(wid)
	# lv.Opt_RemoveRow(0)
	# lv.Opt_Clear()
	print(lv.count())
	lv.setCurrentIndex(lv.model().index(3,0))
	lv.setCurrentIndex(lv.model().index(-1,0))
	lv.Opt_RemoveRow(4)
	lv.indexWidget(lv.model().index(1,0)).Opt_Change(title="AAAAAAAAAAA")
	lv.currentRowChanged.connect(lambda row:print(row,lv.currentIndex()))
	sys.exit(app.exec_())

