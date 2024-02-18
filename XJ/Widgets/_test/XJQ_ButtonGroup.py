
from ..XJQ_ButtonGroup import *

from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QRadioButton,QCheckBox,QWidget

if True:
	app = QApplication([])
	wid=QWidget()
	hbox=QHBoxLayout(wid)
	for item in [
			(QRadioButton,('简单','中等','困难')),
			(QCheckBox,('未下载','收藏','完成','不可用','有记录')),]:
		group=XJQ_ButtonGroup(btnType=item[0])
		for i in item[1]:
			group.Opt_AddButton(i)
		group.stateChanged.connect((lambda group:lambda tx:print(">>",tx,group.Get_CheckedLst()))(group))
		hbox.addWidget(group)
	wid.show()
	app.exec_()
