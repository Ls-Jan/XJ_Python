
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_ButtonGroup import XJQ_ButtonGroup

from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QRadioButton,QCheckBox,QWidget

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		wid=QWidget()
		hbox=QHBoxLayout(wid)
		for item in [
				(QRadioButton,('简单','中等','困难')),
				(QCheckBox,('未下载','收藏','完成','不可用','有记录')),]:
			group=XJQ_ButtonGroup(btnType=item[0])
			for i in item[1]:
				group.Opt_AddButton(i)
			group.stateChanged.connect((lambda group:lambda tx:print(">>",tx,group.Get_CheckedLst()))(group))
			hbox.addWidget(group)
		self.__wid=wid
	def Opt_Run(self):
		self.__wid.show()
		return super().Opt_Run()



