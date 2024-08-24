

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['OpGroup_ExcludeArea']

from .OpGroup_Base import OpGroup_Base
from ....Structs.XJ_Section import XJ_Section
from ..Op.Op_ExcludeArea import Op_ExcludeArea

class OpGroup_ExcludeArea(OpGroup_Base):
	'''
		区间组成的空间将在指定的受限区域之外。
	'''
	def __init__(self,name:str=None):
		super().__init__(name)
		raise Exception('此功能暂未实现')
	def Get_OpCount(self):
		return len(self.__rate)
	def _Core(self,*sections:XJ_Section):
		if(self.Get_OpCount()<len(sections)):
			raise Exception(f"参数个数错误，需传入{self.Get_OpCount()}个XJ_Section对象，实际传入：{sections}")
		super().Opt_Start(*sections)
	



