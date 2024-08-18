

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['Op_Move']

from .Op_Base import Op_Base
from ....Structs.XJ_Section import XJ_Section

class Op_Move(Op_Base):
	'''
		以移动量为curr-old进行区间移动，
		根据XJ_Section.A修改XJ_Section的LR值，
		在XJ_Section.A为0和4时不修改区间。
		通过Set_Disable启用或禁用移动功能
	'''
	__old:int
	__curr:int
	__move:bool
	def __init__(self,pos:int=0):
		super().__init__()
		self.__old=pos
		self.__curr=pos
		self.__move=True
	def Set_Disable(self,flag:bool=True):
		'''
			设置移动禁用
		'''
		self.__move=not flag
	def Get_Pos(self,curr:bool=True):
		'''
			获取点位，如果curr为真则返回当前坐标，否则返回按下时的坐标
		'''
		return self.__curr if curr else self.__old
	def Set_Pos(self,pos:int=None,curr:bool=True):
		'''
			设置位置，如果curr为真则设置__curr，否则设置__old
		'''
		if(curr):
			self.__curr=pos
		else:
			self.__old=pos
	def Opt_Start(self,s:XJ_Section):
		if(self.__move and 0<s.A<4):
			delta=self.__curr-self.__old
			lst=[delta,delta]
			if(s.A==1):
				lst[1]=0
			elif(s.A==3):
				lst[0]=0
			s.L+=lst[0]
			s.R+=lst[1]
		super().Opt_Start(s)
	



