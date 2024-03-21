

from ..XJ_GroupList import XJ_GroupList

if True:
	lst=XJ_GroupList()
	group=(0,)
	lst.Opt_Insert(1,2,group=group)
	lst.Opt_Insert(3,4,group=group)
	lst.Opt_Insert(5,6,group=group)
	lst.Set_GroupName(group,'Test')
	index=5
	print(f'index:{index}    group:{"/".join(lst.Get_ItemGroup(index))}')





