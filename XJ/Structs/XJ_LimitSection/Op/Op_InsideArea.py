

__version__='1.0.0'
__author__='Ls_Jan'

__all__=['Op_InsideArea']

from .Op_Base import Op_Base
from ....Structs.XJ_Section import XJ_Section

class Op_InsideArea(Op_Base):
	'''
		将区间控制在范围内。根据XJ_Section.A对LR进行调整
	'''
	__L:int
	__R:int
	def __init__(self,L:int=None,R:int=None):
		super().__init__()
		self.Set_Section(L,R)
	def Set_Section(self,L:int=None,R:int=None):
		'''
			设置受限区间，传入None不受限(相当于指定为无穷)
		'''
		self.__L=L
		self.__R=R
	def Opt_Start(self,s:XJ_Section):
		mL,mR=self.__L,self.__R
		L,R=sorted([s.L,s.R])
		D=R-L
		if(mL==None):
			if(mR==None):
				mL=L
				mR=R
			else:
				mL=min(mR,R)-D
		elif(mR==None):
			mR=max(mL,L)+D
		elif(mL>mR):
			mL,mR=mR,mL
		LR=[L,R]
		dLR=[[L-mL,L-mR],[R-mL,R-mR]]#正负不变，负负偏左，正正偏右
		whole=s.A%2==0#整体移动
		for i in range(2):
			i=i%2
			d1=dLR[i]
			d2=dLR[(i+1)%2]
			for j in range(2):
				sign=1 if j==0 else -1
				d=d1[j]
				if(sign*d<0):
					LR[i]-=d
					for k in range(2):
						d1[k]-=d
					if(whole):#移动另一端点
						LR[(i+1)%2]-=d
						for k in range(2):
							d2[k]-=d
		d1=dLR[0]
		if(d1[0]*d1[1]>0):#出现同号，直接将L设置为mL
			LR[0]=mL
		s.L,s.R=LR if s.L<s.R else reversed(LR)
		super().Opt_Start(s)
	def Opt_Check(self,s:XJ_Section):
		return XJ_Section(self.__L,self.__R).Get_Intersection(s,returnPos=True)==2



