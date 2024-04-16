
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from ..XJQ_Tag import XJQ_Tag

from PyQt5.QtWidgets import QWidget,QVBoxLayout

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		win=QWidget()

		vbox=QVBoxLayout(win)
		clickTest=False
		index=0
		for style in [
				'Blue',
				'Gray',
				'Orange',
				'Red',
				'Green',
				]:
			tag=XJQ_Tag(style,style,clickable=clickTest or index%2==0,parent=win)
			tag.clicked.connect(lambda val:print(val))
			vbox.addWidget(tag)
			index+=1
			tag.show()
		win.setStyleSheet('background:rgb(20,20,20)')
		self.__win=win

	def Opt_Run(self):
		self.__win.show()
		self.__win.resize(700,400)
		super().Opt_Run()
		return self.__win







