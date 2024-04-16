__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from ..XJ_GroupList import XJ_GroupList


__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		lst=XJ_GroupList()
		group=(0,)
		lst.Opt_Insert(1,2,group=group)
		lst.Opt_Insert(3,4,group=group)
		lst.Opt_Insert(5,6,group=group)
		lst.Set_GroupName(group,'Test')
		index=5
		print(f'index:{index}    group:{"/".join(lst.Get_ItemGroup(index))}')
		return super().Opt_Run()


