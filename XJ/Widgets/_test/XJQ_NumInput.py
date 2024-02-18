
from ..XJQ_NumInput import *

import sys
from PyQt5.QtWidgets import QApplication

if True:
	app = QApplication(sys.argv)

	ni=XJQ_NumInput()
	ni.show()
	
	ni.Set_ValueRange(0,50)
	ni.Set_Precision(1,1)
	ni.Set_Value(17.33)
	ni.valueChanged.connect(lambda i:print(ni.Get_Value()))

	sys.exit(app.exec())


