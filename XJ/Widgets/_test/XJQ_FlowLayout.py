
from ..XJQ_FlowLayout import *
from ..XJQ_Tag import *

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if True:
	app = QApplication(sys.argv)

	wid=QWidget()
	fbox=XJQ_FlowLayout()
	for i in range(10):
		fbox.addWidget(XJQ_Tag(None,str(i)*i+'\n'*(i%2)))
	wid.setMinimumHeight(100)
	wid.setLayout(fbox)
	wid.show()
	fbox.heightChanged.connect(lambda h:print(h))
	wid.resize(500,300)
	sys.exit(app.exec_())
	