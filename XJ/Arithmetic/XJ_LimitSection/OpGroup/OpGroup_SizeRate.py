

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['OpGroup_SizeRate']

from .OpGroup_Base import OpGroup_Base
from ....Structs.XJ_Section import XJ_Section

class OpGroup_SizeRate(OpGroup_Base):
	'''
		使每个区间的长度之间具有比例关系。
		例如调用Set_Rate(3,4,5)然后Opt_Start传入三个XJ_Section，那么这三个XJ_Section长度将会是(3,4,5)的整数/小数倍。
		特别的，优先XJ_Section.A为1或3的区间，
		即传入的XJ_Section长度分别是6、8、15，属性A分别是1、2、3，那么计算出的比值为6/3和15/5，然后根据设置来决定取这两个中的最小值还是最大值
	'''
	__rate:tuple
	__smooth:bool
	__max:bool
	def __init__(self,name:str=None):
		super().__init__(name)
		self.__rate=tuple()
		self.__smooth=True
		self.__max=False
	def Set_MaxResize(self,flag:bool):
		'''
			设置是否以最大比例调整，如果为假则以最小比例调整
		'''
		self.__max=flag
	def Set_Smooth(self,flag:bool):
		'''
			设置是否流畅变化，如果为假则区间长度调整为Rate的整数倍，否则则为小数倍
		'''
		self.__smooth=flag
	def Set_Rate(self,*rate:int):
		'''
			设置长度比例Rate，允许传入None(只要有一个None则大小将不受限)
		'''
		self.__rate=rate
	def Get_OpCount(self):
		return len(self.__rate)
	def _Core(self,*sections:XJ_Section):
		if(len(list(filter(lambda item:item==None,self.__rate)))==0):#rate都不为None才调整大小
			lenLst=[s.R-s.L+1 for s in sections]
			rate=[abs(lenLst[i]/self.__rate[i]) for i in range(len(lenLst))]
			index=[i for i in range(len(sections)) if sections[i].A==1 or sections[i].A==3]
			if(self.__max and len(index)):#【补丁行为，不知道怎么修，只能暂时这样写着，别问，问就是瞎试的】
				rate=[rate[i] for i in index]
			rate=(max if self.__max else min)(rate)
			rate=rate if self.__smooth else int(rate)
			for i in range(len(lenLst)):
				sign=1 if lenLst[i]>0 else -1
				lenLst[i]=sign*int(rate*self.__rate[i]-1)
			for i in range(len(lenLst)):
				s=sections[i]
				if(s.A==1):
					s.L=s.R-lenLst[i]
				elif(s.A==3):
					s.R=s.L+lenLst[i]
				else:
					s.L=int(s.L+s.R-lenLst[i])>>1
					s.R=s.L+int(lenLst[i])
	def _Check(self,*sections:XJ_Section):
		'''
			用于测试sections是否成比例，返回bool
		'''
		# return True
		if(len(list(filter(lambda item:item==None,self.__rate)))==0):#rate都不为None才进行比较
			lenLst=[]
			rate=set()
			for i in range(len(sections)):
				s=sections[i]
				L=s.Get_L()
				R=s.Get_R()
				if(L==None or R==None):
					return True
				lenLst.append(abs(R-L)+1)
				rate.add(lenLst[i]/self.__rate[i])
			if(len(rate)>1):
				return False
			rate=rate.pop()
			if(self.__smooth):
				if(rate!=int(rate)):
					return False
		return True



