
import sys
from PyQt5.QtWidgets import QApplication

from ..XJQ_PageNavigation import *



if True:
	app = QApplication(sys.argv)

	pn=XJQ_PageNavigation(150)
	pn.Set_PerCountList([1,2,3,4,5,10,100])
	pn.resize(250,50)
	pn.changed.connect(lambda start,count:print(start,start+count-1))
	pn.setStyleSheet('''
		color:#FF0000;
		background:#222222;
		margin:0;
	''')
	pn.show()

	sys.exit(app.exec_())
