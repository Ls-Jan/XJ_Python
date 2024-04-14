
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_MarqueeBox import XJQ_MarqueeBox
from ...Functions.GetRealPath import GetRealPath

from PyQt5.QtWidgets import QLabel,QHBoxLayout,QWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QSize


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		lb_1=QLabel()
		path=GetRealPath('./加载动画-7.gif')
		mv=QMovie(path)
		mv.setScaledSize(QSize(250,250))
		mv.start()
		lb_1.setMovie(mv)

		lb_2=QLabel('ABCDEFG\nABCDEFG\nABCDEFG\nABCDEFG')
		lb_2.setStyleSheet('''
			font-size:80px;
		''')

		mq_1=XJQ_MarqueeBox(lb_1,pixel=5,keepOrigin=False,dynamicSnap=True,blankPercent=0,autoSize=False)
		mq_2=XJQ_MarqueeBox(lb_2,delay=0,interval=2,horizontal=False,forward=False,autoSize=False)

		wid=QWidget()
		box=QHBoxLayout(wid)
		box.addWidget(mq_1)
		box.addWidget(mq_2)
		mq_1.setStyleSheet('''
			background:rgba(255,0,0,192);
		''')
		mq_2.setStyleSheet('''
			background:rgba(255,255,0,192);
		''')

		self.__wid=wid
	def Opt_Run(self):
		self.__wid.show()
		self.__wid.resize(500,300)
		return super().Opt_Run()



