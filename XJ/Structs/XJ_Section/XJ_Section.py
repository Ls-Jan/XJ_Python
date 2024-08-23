

__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_Section']

class XJ_Section:
	'''
		区间，记录左值L、右值R，允许L比R大；
		如果P为真则区间将退化为一个点；
		A为Active的缩写，记录哪些点是活动的，有4种取值，分别为0、1、2、3，分别对应：无活动点、活动点L、活动点LR、活动点R。
		当LR赋予None时实际会被赋予Set_NoneValue设置的值(该操作能在不少地方简化代码)
	'''
	__L:float=None
	__R:float=None
	__None:float=(1<<32)-1
	P:bool=None
	A:int=None
	def __init__(self,L:float,R:float,P:bool=False,A:int=0):
		if(P):
			if(A==1):
				L=R
			elif(A==3):
				R=L
			else:
				L=(L+R)>>1
				R=L
		self.L=L
		self.R=R
		self.P=P
		self.A=A
	def __iter__(self):
		'''
			遍历LR的值，或者说用来快速tuple化
		'''
		return iter((self.L,self.R))
	def __eq__(self,section):
		'''
			判断LR值是否一致
		'''
		return self.L==section.L and self.R==section.R
	def __repr__(self):
		'''
			用来Debug，返回形如字串<AAA,[BBB]>，
			方括号代表活动点，
			P为真时尖括号内仅1元素
		'''
		L,R,P,A=self.L,self.R,self.P,self.A
		sL,sR=str(L),str(R)
		if(L<=-self.__None):
			L=None
		if(R>=self.__None):
			R=None
		if(A==1):
			sL=f'[{L}]'
		elif(A==3):
			sR=f'[{R}]'
		elif(A==2):
			sL=f'[{L}'
			sR=f'{R}]'
		if(P):
			return f'<{sL if 1<=A<=2 else sR}>'
		return f'<{sL},{sR}>'
	@property
	def L(self):
		return self.__L
	@property
	def R(self):
		return self.__R
	@L.setter
	def L(self,val:float):
		self.__L=val if val!=None else -self.__None
	@R.setter
	def R(self,val:float):
		self.__R=val if val!=None else self.__None
	def copy(self):
		'''
			创建拷贝
		'''
		return self.__class__(self.L,self.R,self.P,self.A)
	def Get_L(self):
		'''
			与直接获取L不同，该函数在L超出范围时返回None
		'''
		return self.__L if self.__L>=-self.__None else None
	def Get_R(self):
		'''
			与直接获取R不同，该函数在R超出范围时返回None
		'''
		return self.__R if self.__R<=self.__None else None
	def Get_ValuePos(self,val:int,ri:int=0,ro:int=0):
		'''
			获取val在区间的位置，
			ri为内边界宽度，ro为外边界宽度，即val的值在[A-ri,A+ro]内就返回1。

			0：在section左侧；
			1：section在区间左端点处；
			2：section在区间内；
			3：section在区间右端点处；
			4：在section右侧；
		'''
		aL=self.__L-ro
		aR=self.__L+ri
		bL=self.__R-ri
		bR=self.__R+ro
		rst=0
		if(val<aL):
			rst=0
		elif(bR<val):
			rst=4
		else:
			if(aR<val<bL):
				rst=2
			else:
				if(abs(self.__L-val)<abs(self.__R-val)):
					rst=1
				else:
					rst=3
		return rst
	def Get_Intersection(self,section,*,returnPos:bool=False):
		'''
			获取与测试区间的交集，返回XJ_Section对象，如果区间不相交则返回None。

			如果returnPos为真，那么会返回section相对于本区间的位置，用0、1、2、3这四个数来表示，
			数字含义如下(左表示区间LR中的小值，右表示大值)：
				0：在section左侧(不相交)；
				1：section在区间左端点处；
				2：section在区间内，或是区间在section内；
				3：section在区间右端点处；
				4：在section右侧(不相交)；
			数字含义图示：
				0  [1  2  3]  4
		'''
		L,R=sorted((self.L,self.R))
		sL,sR=sorted((section.L,section.R))
		if(L<=-self.__None and sL<=-self.__None):
			sL=1-self.__None
		if(R>=self.__None and sR>=self.__None):
			sR=self.__None-1
		
		if(sR<L):#左侧
			pos=0
		elif(sL<L):
			if(sR<R):#左端点
				pos=1
				R=sR
			else:#包围
				pos=2
		elif(sL<=R):
			if(sR<=R):#内部
				pos=2
				L=sL
				R=sR
			else:#右端点
				pos=3
				L=sL
		else:#右侧
			pos=4
		if(returnPos==False):
			return self.__class__(L,R) if pos%4 else None
		return pos
	def Opt_Sort(self):
		'''
			调整左右值使得L<=R
		'''
		if(self.__L>self.__R):
			self.__L,self.__R=self.__R,self.__L
	@classmethod
	def Set_NoneValue(self,value:float=(1<<32)-1):
		'''
			在对区间端点LR赋值时会将None替换为具体值，
			请设置足够大的值以避免出现奇怪问题。
			最好在创建XJ_Section对象之前调用该函数(如果有需要的话)，否则出现奇怪情况概不负责
		'''
		self.__None=value
	@classmethod
	def Get_NoneValue(self):
		'''
			获取Set_NoneValue设置的值
		'''
		return self.__None




