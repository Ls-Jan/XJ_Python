

# XJQ_ButtonGroup

按钮组，简单的封装，简单
因为出现了“QRadioButton”在选中后无法取消的问题，特此封装，
但只针对这个按钮哪够，除了QRadioButton外，也可以指定QCheckBox复选框按钮

![XJQ_ButtonGroup](../pict/XJQ_ButtonGroup.gif)

```py

from XJ.Widgets import XJQ_ButtonGroup 

from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QRadioButton,QCheckBox,QWidget

if True:
	app = QApplication([])
	wid=QWidget()
	hbox=QHBoxLayout(wid)
	for item in [
			(QRadioButton,('简单','中等','困难')),
			(QCheckBox,('未下载','收藏','完成','不可用','有记录')),]:
		group=XJQ_ButtonGroup(btnType=item[0],layout=QVBoxLayout)
		for i in item[1]:
			group.Opt_AddButton(i)
		group.changed.connect((lambda group:lambda tx:print(">>",tx,group.Get_CheckedLst()))(group))
		hbox.addWidget(group)
	wid.show()
	app.exec_()

```
