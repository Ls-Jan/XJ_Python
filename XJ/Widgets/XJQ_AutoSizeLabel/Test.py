
__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from ...ModuleTest import XJQ_Test
from .XJQ_AutoSizeLabel import XJQ_AutoSizeLabel

from PyQt5.QtGui import QMovie,QPixmap
from XJ.Functions.GetRealPath import GetRealPath

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		lb=XJQ_AutoSizeLabel()
		pix=QPixmap(GetRealPath('图标-剪贴板.png'))
		lb.setPixmap(pix)
		lb.Set_PictResize(1.5)
		# lb.Set_AutoSize(True)
		lb.show()

		self.__lb=lb
	def Opt_Run(self):
		self.__lb.show()
		super().Opt_Run()



