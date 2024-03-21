from ..XJQ_ComboBox import *

import sys
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QApplication,QPushButton


if True:
	app = QApplication(sys.argv)

	cb=XJQ_ComboBox()
	cb.indexChanged.connect(lambda index,text:print(index,text))

	num=[0,10]
	def Refresh(num):
		cb.clear()
		cb.Set_List([str(i) for i in range(*num)])
		diff=num[1]-num[0]
		num[0]=num[1]
		num[1]+=diff
	btn=QPushButton('Refresh')
	btn.clicked.connect(lambda:Refresh(num))

	wid=QWidget()
	hbox=QHBoxLayout(wid)
	hbox.addStretch(1)
	hbox.addWidget(cb)
	hbox.addWidget(btn)
	hbox.addStretch(1)
	wid.show()

	style='''
			QComboBox{
				font-size:20px;
				color:rgba(0,0,0,255);
				background:rgba(96,192,255,192);
				border-radius:10px;
				min-width:50px;
				text-align:center;
			}
			QComboBox::drop-down{
				width:0;
				image:none;
			}

			QComboBox QAbstractItemView {
				font-size:25px;
				min-width: 50px;
				font-weight:0;
				font-family:serif;
				background-color: rgba(224, 224, 128, 255);
			}
			QComboBox QAbstractItemView::item {
				height: 30px;
				background-color: rgba(237, 0, 0,128);
			}

			QComboBox QScrollBar
			{
				background: rgba(255,255,255,5%);
				width: 5px;
			}
			QComboBox QScrollBar::add-line {
				width:0;
				height:0;
			}
			QComboBox QScrollBar::sub-line {
				width:0;
				height:0;
			}
			QComboBox QScrollBar::handle {
				background: rgba(64,64,64,75%);
			}
			QComboBox QScrollBar::sub-page {
				background: rgba(0,0,0,30%);
			}
			QComboBox QScrollBar::add-page {
				background: rgba(0,0,0,30%);
			}
		'''

	# cb.setStyleSheet(style)

	sys.exit(app.exec_())

