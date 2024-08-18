

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['Op_Flippable']

from .Op_Base import Op_Base
from ....Structs.XJ_Section import XJ_Section

class Op_Flippable(Op_Base):
	'''
		是否允许翻转，或者说就是左边界能否跨越右边界
	'''
	__flippable:bool
	def __init__(self,flag:bool=True):
		super().__init__()
		self.Set_Flippable(flag)
	def Set_Flippable(self,flag:bool):
		'''
			设置是否允许翻转
		'''
		self.__flippable=flag
	def Opt_Start(self,s:XJ_Section):
		if(self.__flippable==False and s.L>s.R):
			if(s.A>1):
				s.R=s.L
			else:
				s.L=s.R
		super().Opt_Start(s)
	



