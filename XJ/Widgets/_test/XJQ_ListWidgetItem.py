from ..XJQ_ListWidgetItem import *
from ..XJQ_PureColorIcon import *
from ...Functions.GetRealPath import *

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout

if True:
	app = QApplication(sys.argv)

	icons=[
		XJQ_PureColorIcon(GetRealPath('../../Icons/收藏.png'),size=(20,20)),
		XJQ_PureColorIcon(GetRealPath('../../Icons/云锁-002.png'),size=(20,20)),
		XJQ_PureColorIcon(GetRealPath('../../Icons/对勾.png'),size=(20,20)),
		XJQ_PureColorIcon(GetRealPath('../../Icons/文件袋.png'),size=(20,20)),
		XJQ_PureColorIcon(GetRealPath('../../Icons/云下载.png'),size=(20,20)),
		XJQ_PureColorIcon(GetRealPath('../../Icons/已锁.png'),size=(20,20)),]
	icons[0].Set_Color((255,0,255,192))
	icons[1].Set_Color((255,0,0,192))
	icons[2].Set_Color((0,255,0,192))
	icons[3].Set_Color((0,255,255,192))
	icons[4].Set_Color((255,255,0,192))

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

