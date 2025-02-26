
'''
	使用QSignalMapper将多个按钮的点击事件绑定到同一个函数上
'''


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


if True:
	app=QApplication([])

	wid=QWidget()
	box=QHBoxLayout(wid)
	smp=QSignalMapper()
	for i in range(3):
		btn=QPushButton(str(i))
		btn.resize(100,100)
		btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding))
		box.addWidget(btn)
		btn.clicked.connect(smp.map)
		smp.setMapping(btn,btn)#设置映射，第二参数即为传给目标槽函数(mapped)的参数
	smp.mappedWidget.connect(lambda btn:print(">",btn.text()))#使用的是mappedWidget而非mapped

	wid.show()
	wid.resize(600,200)
	app.exec()
	exit()











