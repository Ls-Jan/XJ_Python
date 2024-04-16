
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_ComboBox import XJQ_ComboBox

from PyQt5.QtWidgets import QWidget,QHBoxLayout,QPushButton


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		cb=XJQ_ComboBox()
		cb.indexChanged.connect(lambda index,text:print(index,text))

		num=[0,20]
		def Refresh(num):
			cb.clear()
			cb.Set_List([str(i) for i in range(*num)])
			diff=num[1]-num[0]
			num[0]=num[1]
			num[1]+=diff
		btn=QPushButton('Refresh')
		btn.clicked.connect(lambda:Refresh(num))
		Refresh(num)

		wid=QWidget()
		hbox=QHBoxLayout(wid)
		hbox.addStretch(1)
		hbox.addWidget(cb)
		hbox.addWidget(btn)
		hbox.addStretch(1)
		self.__wid=wid
		self.__cb=cb

	def Opt_Run(self):
		print('可尝试滚轮调整当前值')
		self.__wid.show()
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
		# self.__cb.setStyleSheet(style)
		super().Opt_Run()
		# return self.__wid


