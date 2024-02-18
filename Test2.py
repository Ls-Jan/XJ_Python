
from PyQt5.QtCore import QTimerEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os
from XJ.Structs.XJ_GIFMaker import *
from XJ.Widgets.XJQ_PictCarousel import *

class Test(QWidget):
	def timerEvent(self, a0: QTimerEvent) -> None:
		# QApplication.setActiveWindow(self)
		print("TTT")
		self.activateWindow()
		return super().timerEvent(a0)

if True:
	app = QApplication([])
	t=Test()
	t.setFocusPolicy(Qt.StrongFocus)
	tr=t.startTimer(500)
	t.show()
	wid=QPushButton("TEST")
	wid.show()
	app.exec_()

if True:
	app = QApplication([])

	#QListView显示图标：https://blog.csdn.net/weixin_42193704/article/details/122424223
	model=QStandardItemModel()
	lv=QListView()
	lv.resize(600,400)
	lv.setModel(model)
	lv.setIconSize(QSize(64,64))
	lv.doubleClicked.connect(lambda item:print(item.row()))
	lv.pressed.connect(lambda item:print(item.row()))

	# file='2024-01-09 00-15-45.mp4'
	file='Clock_JE3_BE3.webp'
	# file='加载动画-7.gif'
	file=os.path.join('F:/文档/Videos',file)

	gm=XJ_GIFMaker()
	size=gm.Opt_LoadSource(file)
	print(size)
	frames=[QPixmap(QImage(f.data,*size, size[0]*4,QImage.Format_RGBA8888)) for f in gm.frames]
	
	t=XJQ_PictCarousel()
	t.Set_Frames(frames)
	t.Opt_Play(True)
	t.Set_Duration(gm.duration)
	t.Set_Loop(gm.duration)
	i=0
	for f in frames:
		# item=QStandardItem(XJQ_Icon(f),'TTT')
		i+=1
		item=QStandardItem(QIcon(f),str(i).zfill(len(str(len(frames)))))
		item.setCheckable(True)
		item.setEditable(False)
		model.appendRow(item)

	win=QWidget()
	win.resize(1000,600)
	win.show()
	hbox=QHBoxLayout(win)
	hbox.addWidget(lv)
	hbox.addWidget(t,1)
	# t.setStyleSheet('background:#222222;')

	app.exec_()

