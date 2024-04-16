
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_FlowLayout import XJQ_FlowLayout
from ..XJQ_Tag import XJQ_Tag

from PyQt5.QtWidgets import QWidget

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		wid=QWidget()
		self.__wid=wid
		fbox=XJQ_FlowLayout()
		for i in range(10):
			tag=XJQ_Tag(str(i)*i+'\n'*(i%2))
			fbox.addWidget(tag)
		# for tag in fbox.Get_WidgetLst(4):
			# fbox.removeWidget(tag)#移除
		wid.setMinimumHeight(100)
		wid.setLayout(fbox)
		# fbox.heightChanged.connect(lambda h:print(h))
	def Opt_Run(self):
		self.__wid.show()
		self.__wid.resize(500,300)
		super().Opt_Run()
		# return self.__wid




