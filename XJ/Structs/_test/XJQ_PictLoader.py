
from ..XJ_Frame import *
from ..XJ_GIFMaker import *
from ..XJQ_PictLoader import *
from ...Functions.GetRealPath import *

from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QPushButton,QListView
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QIcon
from PyQt5.QtCore import QSize


from ...Functions.CV2ToQPixmap import *

if True:
	app=QApplication([])
	wid=QWidget()
	vbox=QVBoxLayout(wid)
	btnL=QPushButton('Load')
	btnC=QPushButton('Clear')
	lv=QListView()
	vbox.addWidget(btnL)
	vbox.addWidget(btnC)
	vbox.addWidget(lv)
	wid.show()
	file=GetRealPath('../../Icons/Loading/加载动画-7.gif')
	lvModel=QStandardItemModel()
	lv.setModel(lvModel)
	lv.setIconSize(QSize(64,64))
	gm=XJ_GIFMaker()
	gm.Opt_Insert(file)
	for i in range(len(gm.frames)):
		lvModel.appendRow(QStandardItem(str(i)))

	pl=XJQ_PictLoader()
	pl.loaded.connect(lambda id,pix:lvModel.item(id).setIcon(QIcon(pix)))
	btnL.clicked.connect(lambda:pl.Opt_Append(*[(i,gm.frames[i]) for i in range(len(gm.frames))]))
	btnC.clicked.connect(lambda:pl.Opt_Clear() or [lvModel.item(i).setIcon(QIcon()) for i in range(len(gm.frames))])

	wid.resize(800,400)
	app.exec()
	exit()

