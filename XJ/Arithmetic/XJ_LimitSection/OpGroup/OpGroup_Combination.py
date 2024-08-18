

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['OpGroup_Combination']

from .OpGroup_Base import OpGroup_Base
from ....Structs.XJ_Section import XJ_Section
from ..Op.Op_Base import Op_Base

class OpGroup_Combination(OpGroup_Base):
	'''
		使用组合模式，可以添加多个Op_Base派生对象
	'''
	__lst:list
	def __init__(self,name:str=None):
		super().__init__(name)
		self.__lst=[]
	def Set_OpLst(self,*opLst:Op_Base):
		'''
			设置Op列表
		'''
		self.__lst=opLst
	def Get_OpLst(self):
		'''
			返回Op列表
		'''
		return list(self.__lst)
	def Get_OpCount(self):
		'''
			获取Op个数
		'''
		return len(self.__lst)
	def _Core(self,*sections:XJ_Section):
		for i in range(len(sections)):
			self.__lst[i].Opt_Start(sections[i])
	def _Check(self,*sections:XJ_Section):
		for i in range(len(sections)):
			if(self.__lst[i].Opt_Check(sections[i])==False):
				return False
		return True




