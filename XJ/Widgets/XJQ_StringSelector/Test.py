
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['Test']

from ...ModuleTest import XJQ_Test
from .XJQ_StringSelector import XJQ_StringSelector

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		ss=XJQ_StringSelector()
		self.__ss=ss
		lst=['1','2','3','4']
		ss.Set_DisableList(lst)
		ss.Set_SelectableList(lst)
		ss.createNewString.connect(lambda key:None if key.isdigit() else ss.Opt_CancelLastString())
	def Opt_Run(self):
		lv=self.__ss.Get_ListView()
		# lv.edit(lv.model().index(lv.model().rowCount()-1,0))
		lv.show()

		super().Opt_Run()
		return self.__ss











