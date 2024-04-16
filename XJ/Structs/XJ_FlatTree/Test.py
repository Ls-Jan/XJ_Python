__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .XJ_FlatTree import XJ_FlatTree


__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		tr=XJ_FlatTree()
		node=tr.Get_RootNode()
		node=tr.Opt_CreateNext(node,'A')
		tr.Opt_CreateNext(node,'A1')
		tr.Opt_CreateNext(node,'A2')
		node=tr.Opt_CreateNext(node,'AB')
		tr.Opt_CreateNext(node,'AB1')
		tr.Opt_CreateNext(node,'AB2')
		tr.Opt_CreateNext(node,'AB3')
		node=tr.Get_RootNode()
		tr.Opt_CreateNext(node,'X')
		node=tr.Opt_CreateNext(node,'Y')
		tr.Opt_CreateNext(node,'Y1')
		tr.Opt_CreateNext(node,'Y2')
		tr.Opt_CreateNext(node,'Y3')

		i=0
		for n in tr.data():
			print(i,n)
			i+=1
		print()

		tr.Opt_RemoveNode(list(tr.Opt_SearchNodes('AB'))[0])

		i=0
		for n in tr.data():
			print(i,n)
			i+=1
		return super().Opt_Run()


