

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['Op_LimitLen']

from .Op_Base import Op_Base
from ....Structs.XJ_Section import XJ_Section

class Op_LimitLen(Op_Base):
	'''
		决定区间最小最大长度，当XJ_Section.P为真时不对区间进行改动
	'''
	__minLen:int
	__maxLen:int
	def __init__(self,minLen:int=None,maxLen:int=None):
		super().__init__()
		self.Set_MinLength(minLen)
		self.Set_MaxLength(maxLen)
	def Set_MinLength(self,length:int):
		'''
			设置最小区间长度，传入None则不受限
		'''
		self.__minLen=length
	def Set_MaxLength(self,length:int):
		'''
			设置最大区间长度，传入None则不受限
		'''
		self.__maxLen=length
	def Opt_Start(self,s:XJ_Section):
		if(not s.P):
			oldLen=abs(s.R-s.L)+1
			newLen=oldLen
			if(self.__minLen!=None):
				if(newLen<self.__minLen):
					newLen=self.__minLen
			if(self.__maxLen!=None):
				if(newLen>self.__maxLen):
					newLen=self.__maxLen
			if(oldLen!=newLen):
				newLen-=1
				sign=1 if s.L<s.R else -1
				newLen*=sign
				if(s.A==1):
					s.L=s.R-newLen
				elif(s.A==3):
					s.R=s.L+newLen
				else:
					s.L=(s.L+s.R-newLen)/2
					s.R=s.L+newLen
		super().Opt_Start(s)
	def Opt_Check(self,s:XJ_Section):
		newLen=abs(s.R-s.L)+1
		if(self.__minLen!=None):
			if(newLen<self.__minLen):
				return False
		if(self.__maxLen!=None):
			if(newLen>self.__maxLen):
				return False
		

