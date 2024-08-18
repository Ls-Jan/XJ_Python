

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['Op_AsPoint']

from .Op_Base import Op_Base
from ....Structs.XJ_Section import XJ_Section

class Op_AsPoint(Op_Base):
	'''
		根据XJ_Section.P将区间退化为一个点
	'''
	def __init__(self):
		super().__init__()
	def Opt_Start(self,s:XJ_Section):
		L,R,P,A=s.L,s.R,s.P,s.A
		if(P):
			if(A==1):
				L=R
			elif(A==3):
				R=L
			else:
				L=(L+R)>>1
				R=L
		s.L=L
		s.R=R
		super().Opt_Start(s)
	



