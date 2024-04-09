

from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout
from PyQt5.QtCore import Qt
from ..XJQ_SearchBox import XJQ_SearchBox

if True:
	app = QApplication([])

	sb=XJQ_SearchBox()
	sb.Set_StandbyList([f'{i}' for i in range(1000)],Qt.MatchFlag.MatchStartsWith)
	sb.commited.connect(lambda tx:print(f">>>>>>[{tx}]"))
	sb.Set_Size(18)
	print('尝试输入数字')
	# sb.updated.connect(lambda tx:sb.Set_StandbyList(['aaa','aab']))
	# sb.show()

	wid=QWidget()
	hbox=QHBoxLayout(wid)
	hbox.addWidget(sb)
	wid.show()
	sb.Set_Focus()

	app.exec_()




