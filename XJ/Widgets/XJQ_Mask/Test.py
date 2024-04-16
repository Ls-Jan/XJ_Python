
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_Mask import XJQ_Mask
from ..XJQ_LoadingAnimation import XJQ_LoadingAnimation

from PyQt5.QtWidgets import QListView
from PyQt5.QtCore import QStringListModel

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		lv=QListView()
		lv.setModel(QStringListModel([str(i) for i in range(10)]))

		la=XJQ_LoadingAnimation()
		mk=XJQ_Mask(lv,centerWidget=la)
		mk.clicked.connect(lambda:print('遮罩被点击'))

		self.__wid=lv
	def Opt_Run(self):
		self.__wid.resize(600,400)
		self.__wid.show()
		super().Opt_Run()
		return self.__wid




