from ..XJQ_ListWidgetItem import XJQ_ListWidgetItem
from ..XJQ_PureColorIcon import XJQ_PureColorIcon
from ...Functions.GetRealPath import GetRealPath

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout

if True:
	app = QApplication(sys.argv)
	iconSize_1=(24,24)
	iconSize_2=(40,40)
	icons=[
		XJQ_PureColorIcon('../../Icons/收藏.png',size=iconSize_1,fg=(255,0,255,192)),
		XJQ_PureColorIcon('../../Icons/云错误.png',size=iconSize_2,fg=(255,0,0,192)),
		XJQ_PureColorIcon('../../Icons/对勾.png',size=iconSize_1,fg=(0,255,0,192)),
		XJQ_PureColorIcon('../../Icons/文件袋.png',size=iconSize_1,fg=(0,255,255,192)),
		XJQ_PureColorIcon('../../Icons/云下载.png',size=iconSize_2,fg=(255,255,0,192)),
		XJQ_PureColorIcon('../../Icons/已锁.png',size=iconSize_1),]

	wid=QWidget()
	vbox=QVBoxLayout(wid)
	lst=[
		('测试1',['标签1','标签2'],'rgba(255,160,0,128)',),
		('测试2',['标签1','标签2'],'rgba(255,0,0,128)',(icons[1],)),
		('测试3',['标签1','标签2','标签3','标签4'],'rgba(0,0,255,128)',(icons[0],icons[2],icons[3],)),
		('测试4',['标签1','标签2'],'rgba(255,160,0,128)',(icons[4],)),
		('测试5',['标签1','标签2'],'rgba(0,0,255,128)',(icons[0],)),
		]
	for data in lst:
		vbox.addWidget(XJQ_ListWidgetItem(*data))
	wid.show()
	wid.resize(300,400)
	wid.setStyleSheet('background:#222222')

	sys.exit(app.exec_())

