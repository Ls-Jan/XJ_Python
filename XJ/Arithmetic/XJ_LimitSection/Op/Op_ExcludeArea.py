

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['Op_ExcludeArea']

from .Op_Base import Op_Base
from ....Structs.XJ_Section import XJ_Section

class Op_ExcludeArea(Op_Base):
	'''
		限制区间s边界的不可落入范围eA。
		附加一个Include属性，在eA两侧有界时如果Include属性为真则区间s一定包含范围eA
	'''
	__L:int
	__R:int
	__I:bool
	def __init__(self,L:int=None,R:int=None,I:bool=False):
		super().__init__()
		raise Exception('此功能暂未实现')
		self.Set_Section(L,R)
		self.Set_IncludeSection(I)
	def Set_Section(self,L:int=None,R:int=None):
		'''
			设置受限区间，传入None则不受限
		'''
		self.__L=L
		self.__R=R
	def Set_IncludeSection(self,flag:bool):
		'''
			是否令目标区间包含受限区间
		'''
		self.__I=flag
	def Opt_Start(self,s:XJ_Section):
		sign=1 if s.L<s.R else -1
		sL,sR=sorted([s.L,s.R])
		L=self.__L
		R=self.__R
		I=self.__I
		if(I!=None):
			if(sL>L):
				sL=L
			if(sR<R):
				sR=R
		else:
			if(sL<L and sR>L):
				sR=L
			if(sL<R and sR>R):
				sL=R
		sL,sR=sL,sR if sign>0 else sR,sL
		self.L=sL
		self.R=sR
		super().Opt_Start(s)
	def Opt_Check(self,s:XJ_Section):
		return True



