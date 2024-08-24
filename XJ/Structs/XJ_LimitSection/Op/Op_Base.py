

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['Op_Base']


from ....Structs.XJ_Section import XJ_Section

class Op_Base:
	'''
		区间操作类。
		此为基类，调用Opt_Start和Opt_Check无实际作用。
		Opt_Check用于检测区间是否满足条件，按需重写
	'''
	def __init__(self):
		pass
	def Opt_Start(self,s:XJ_Section):
		pass
	def Opt_Check(self,s:XJ_Section):
		return True



