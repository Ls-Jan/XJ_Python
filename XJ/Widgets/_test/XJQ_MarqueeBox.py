from ..XJQ_MarqueeBox import *
from ...Functions import GetRealPath

import sys
from PyQt5.QtWidgets import QApplication,QLabel,QHBoxLayout,QWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QSize

if True:
	app = QApplication(sys.argv)

	lb_1=QLabel()
	path=GetRealPath('../icons/加载动画-7.gif')
	mv=QMovie(path)
	mv.start()
	mv.setScaledSize(QSize(250,250))
	lb_1.setMovie(mv)

	lb_2=QLabel('ABCDEFG\nABCDEFG\nABCDEFG\nABCDEFG')
	lb_2.setStyleSheet('''
		font-size:80px;
	''')


	mq_1=XJQ_MarqueeBox(lb_1,pixel=5,keepOrigin=False,dynamicSnap=True,blankPercent=0,autoSize=False)
	mq_2=XJQ_MarqueeBox(lb_2,delay=0,interval=2,horizontal=False,forward=False,autoSize=False)
	wid=QWidget()
	wid.show()
	wid.resize(500,300)
	box=QHBoxLayout(wid)
	box.addWidget(mq_1)
	box.addWidget(mq_2)
	mq_1.setStyleSheet('''
		background:rgba(255,0,0,192);
	''')
	mq_2.setStyleSheet('''
		background:rgba(255,255,0,192);
	''')

	sys.exit(app.exec_())

