
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_NumInput import XJQ_NumInput


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		ni=XJQ_NumInput()
		ni.Set_ValueRange(0,50)
		# ni.Set_Precision(10,1)
		ni.Set_Precision(0.1,1)
		ni.Set_Value(17.33)
		ni.valueChanged.connect(lambda i:print(ni.Get_Value()))

		self.__ni=ni
	def Opt_Run(self):
		self.__ni.show()
		return super().Opt_Run()








