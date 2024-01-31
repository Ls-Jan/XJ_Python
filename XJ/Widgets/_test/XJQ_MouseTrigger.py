
from ..XJQ_MouseTrigger import *

from PyQt5.QtWidgets import QApplication,QPushButton,QWidget,QLabel
from PyQt5.QtCore import QRect

if True:
	app = QApplication([])

	win=QWidget()
	win.resize(400,400)
	win.show()
	lb=QLabel("移动鼠标",win)
	lb.setGeometry(QRect(150,150,100,100))
	lb.show()
	btn=QPushButton("Test",win)
	btn.setGeometry(QRect(100,100,200,200))
	btn.clicked.connect(lambda:print("CLICK"))
	btn.hide()
	mt=XJQ_MouseTrigger(win)
	# mt.Opt_AddRange('Center',(0.25,0.25),(0.5,0.5))
	mt.Opt_AddRange('Left',(0,0),(100,1.0))
	mt.Opt_AddRange('Btn',target=btn)

	def Func(name,enter):
		print('->Enter' if enter else 'Leave',name)
		if(name=='Btn'):
			if(enter):
				btn.show()
			else:
				btn.hide()
	mt.enter.connect(Func)



	app.exec_()


