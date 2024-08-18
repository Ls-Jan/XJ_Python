

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['OpGroup_Base']
from ....Structs.XJ_Section import XJ_Section

class OpGroup_Base:
	'''
		操作组。

		使用责任链模式，
		派生类需重写_Core和Get_OpCount，
		不需要重写Opt_Start，
		选择重写Opt_Check。
	'''
	__next=None
	__disable=False
	__name=None
	__debug=False
	def __init__(self,name:str=None):
		self.__name=name if name else self.__class__.__name__
	def Set_Disable(self,flag:bool=True):
		'''
			是否禁止在Opt_Start中调用_Core
		'''
		self.__disable=flag
	def Set_Debug(self,flag:bool):
		'''
			用于debug，在debug模式下调用Opt_Start的过程中会输出XJ_Section的前后变化。
			(实际上并不好用
		'''
		self.__debug=flag
	def Set_Next(self,next):
		'''
			设置下个OpGroup对象
		'''
		self.__next=next
	def Get_OpCount(self):
		'''
			获取操作数，以便判断Opt_Start传入的参数个数是否异常。-1代表无限制
		'''
		return -1
	def Get_Name(self):
		'''
			返回初始化时传入的name，便于debug查错
		'''
		return self.__name
	def Opt_Check(self,*sections:XJ_Section):
		'''
			同Opt_Start，只不过以检测为主，
			当sections不满足节点设立条件时会返回对应节点。
		'''
		if(self._Check(*sections)==False):
			return self
		return self.__next.Opt_Check(*sections) if self.__next else None
	def Opt_Start(self,*sections:XJ_Section,debug:bool=False):
		'''
			传入XJ_Section列表，参数个数若与内部的操作数不一致则抛出异常。
			会链式调用，通过Set_Next设置下一节点。
			在debug为真时，指定节点如果通过Set_Debug设置debug那么将会输出XJ_Section的前后变化
		'''
		opCount=self.Get_OpCount()
		if(opCount>=0 and opCount!=len(sections)):
			raise Exception(f"参数个数错误，{self.__class__}需传入{opCount}个XJ_Section对象，实际传入：{sections}")
		if(not self.__disable):
			if(debug and self.__debug):
				print(f'[{self.__name}]'.ljust(30),end=' ')
				print(sections,end=' ')
				self._Core(*sections)
				print(sections)
			else:
				self._Core(*sections)
		if(self.__next):
			self.__next.Opt_Start(*sections,debug=debug)
		elif(debug):
			print()
	def _Core(self,*sections:XJ_Section):
		'''
			在Opt_Start中被调用，
			该函数没有显式调用的必要，
			派生类需对该函数进行重写
		'''
		pass
	def _Check(self,*sections:XJ_Section):
		'''
			在Opt_Check中被调用，
			该函数没有显式调用的必要，
			派生类需对该函数进行重写
		'''
		pass



