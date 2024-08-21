

__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_RectResize']

from XJ.Structs.XJ_Section import XJ_Section
from XJ_LimitSection.Op import Op_Move
from XJ_LimitSection.Op import Op_Flippable
from XJ_LimitSection.Op import Op_AsPoint
from XJ_LimitSection.Op import Op_InsideArea
from XJ_LimitSection.Op import Op_LimitLen
from XJ_LimitSection.OpGroup import OpGroup_Combination
from XJ_LimitSection.OpGroup import OpGroup_SizeRate
from XJ_LimitSection.OpGroup import OpGroup_Base
# from XJ_LimitSection.OpGroup import OpGroup_ExcludeArea#【该模块不使用，因为没做】

class XJ_RectResize:
	'''
		矩形大小调整。
		将区域拖拽截取行为抽象为本类。

		具有的特殊功能如下：
			- Set_LimitArea：限制选定区域；
			- Set_LimitSize：限定选区的最大最小宽高；
			- Set_SizeRate：设置宽高比；
			- Set_SmoothResize：在宽高比给定时决定是否流畅缩放，详见函数说明；
			- Set_Flippable：选区边界拖拽时是否允许翻转，详见函数说明；
	'''
	def __init__(self):
		opMove=[Op_Move(),Op_Move()]
		opPoint=[Op_AsPoint(),Op_AsPoint()]
		opFlip=[Op_Flippable(),Op_Flippable()]
		opLimit=[Op_LimitLen(),Op_LimitLen()]
		opInside=[Op_InsideArea(),Op_InsideArea()]
		stepMove=OpGroup_Combination('stepMove')
		stepPoint=OpGroup_Combination('stepPoint')
		stepFlip=OpGroup_Combination('stepFlip')
		stepLimit=OpGroup_Combination('stepLimit')
		stepInside=OpGroup_Combination('stepInside')
		stepResizeMin=OpGroup_SizeRate('stepResizeMin')
		stepResizeMax=OpGroup_SizeRate('stepResizeMax')
		stepStart=OpGroup_Base('stepStart')
		sections=[XJ_Section(0,0),XJ_Section(0,0)]
		#属性
		self.__opMove=opMove
		self.__opFlip=opFlip
		self.__opLimit=opLimit
		self.__opInside=opInside
		self.__stepResizeMin=stepResizeMin
		self.__stepResizeMax=stepResizeMax
		self.__stepStart=stepStart
		self.__sections=sections
		self.__sectionsOld=sections
		#其他数据
		self.__borderThick=4#边界厚度
		self.__exist=False#矩形是否存在
		self.__press=False#鼠标是否按下
		#属性配置
		stepMove.Set_OpLst(*opMove)
		stepPoint.Set_OpLst(*opPoint)
		stepFlip.Set_OpLst(*opFlip)
		stepLimit.Set_OpLst(*opLimit)
		stepInside.Set_OpLst(*opInside)
		stepResizeMin.Set_Rate(None,None)
		stepResizeMax.Set_Rate(None,None)
		stepResizeMin.Set_MaxResize(False)
		stepResizeMax.Set_MaxResize(True)
		#设置调用顺序
		chain=[
			stepStart,
			stepPoint,
			stepMove,
			stepFlip,
			stepResizeMax,
			stepLimit,
			stepResizeMin,
			stepInside,
		]
		for i in range(1,len(chain)):
			chain[i-1].Set_Next(chain[i])
		# debug=[
		# 	stepStart,
		# 	stepPoint,
		# 	stepMove,
		# 	stepFlip,
		# 	stepResizeMax,
		# 	stepLimit,
		# 	stepResizeMin,
		# 	stepInside,
		# ]
		# for step in debug:
		# 	step.Set_Debug(True)
	def Opt_Move(self,x:int,y:int):
		'''
			移动鼠标当前位置
		'''
		xy=[x,y]
		for i in range(2):
			self.__opMove[i].Set_Pos(xy[i])
		if(self.__press):#拖拽
			self.__exist=self.Opt_Update() or self.__exist
		else:#移动
			anchor=self.Get_HoverPos(dim=True)
			for i in range(2):
				self.__sections[i].A=anchor[i]
	def Opt_Press(self):
		'''
			按键按下。在按键已按下时调用无效
		'''
		if(not self.__press):#防止重复调用
			xy=[self.__opMove[i].Get_Pos() for i in range(2)]
			if(self.__exist):#矩形存在
				secA=[self.__sections[i].A for i in range(2)]
				if(secA[0]==2 or secA[1]==2):
					for i in range(2):
						if(secA[i]!=2):
							self.__sections[(i+1)%2].A=0
				self.__sectionsOld=self.__sections
			else:
				for i in range(2):
					sc=self.__sectionsOld[i]
					p=xy[i]
					sc.L=p
					sc.R=p
					sc.A=3
			for i in range(2):
				self.__opMove[i].Set_Pos(xy[i],False)
			self.__exist=self.Opt_Update() or self.__exist
			self.__press=True
	def Opt_Release(self):
		'''
			按键抬起。
		'''
		for i in range(2):
			s=self.__sections[i]
			s.L,s.R=sorted([s.L,s.R])
		self.__press=False
	def Opt_Update(self):
		'''
			更新矩形，一般不需要显式调用。
			更新失败则返回False
		'''
		test=[self.__sectionsOld[i].copy() for i in range(2)]
		self.__stepStart.Opt_Start(*test)
		node=self.__stepStart.Opt_Check(*test)
		# self.__stepStart.Opt_Start(*test,debug=True)
		# print(">>>",node.Get_Name() if node else 'None')
		if(node==None):
			self.__sections=test
			return True
		return False
	def Opt_ClearRect(self):
		'''
			清除矩形
		'''
		self.__exist=False
	def Get_IsPressed(self):
		'''
			判断鼠标是否按下拖拽
		'''
		return self.__press
	def Get_HoverPos(self,adjust:bool=True,dim:bool=False):
		'''
			获取鼠标悬浮边，将返回数字0-9中的一个数。
			如果adjust为真，则L>R时LR值互换，TB同理，以便设置正确的鼠标光标。
			如果dim为真，将位置分成两个维度对应x轴和y轴，返回两个数字，取值0-3，含义同XJ_Section.A。

			数字含义如下：
				0：当前位置在矩形之外；
				5：当前位置在矩形内部；
				123：在矩形的上边；
				147：在矩形的左边；
				369：在矩形的右边；
				789：在矩形的下边；

			数字的含义用图表示如下：
				1  2  3
				4  5  6
				7  8  9
				   0
		'''
		rst=[0,0]
		if(self.__exist):
			W=self.__borderThick
			W1=W/2
			W2=W-W1-1
			xy=[self.__opMove[i].Get_Pos(True) for i in range(2)]
			for i in range(2):
				sc=self.__sections[i]
				p=sc.Get_Intersection(XJ_Section(xy[i]-W1,xy[i]+W2),returnPos=True)
				p=p if adjust or sc.L<sc.R else 4-p
				if(p%4==0):
					rst=[0,0]
					break
				if(p==2 and abs(sc.L-sc.R)<=W and sc.P==False):#贴太紧，以最近边为准
					p=1 if abs(sc.L-xy[i])<abs(sc.R-xy[i]) else 3
				rst[i]=p
		if(not dim):
			rst=5+sum([(rst[i]-2)*(pow(3,i)) for i in range(2)])
		return rst
	def Get_Rect(self,adjust:bool=True):
		'''
			获取矩形，返回LTRB，如果矩形不存在则返回None。
			如果adjust为真，在L>R时会将LR的值对换，TB同理
		'''
		if(self.__exist):
			L,R=self.__sections[0]
			T,B=self.__sections[1]
			if(adjust):
				L,R=sorted([L,R])
				T,B=sorted([T,B])
			return [L,T,R,B]
		return None
	def Set_OnlyPoint(self,flag:bool):
		'''
			如果该值为真则矩形将退化为一个像素点
		'''
		for section in self.__sections:
			section.P=flag
		self.Opt_Update()
	def Set_Rect(self,L:int=0,T:int=0,R:int=0,B:int=0):
		'''
			设置矩形，不一定总能设置成功
		'''
		lst=[(L,R),(T,B)]
		for i in range(2):
			self.__sectionsOld[i].L=lst[i][0]
			self.__sectionsOld[i].R=lst[i][1]
		flag=self.Opt_Update()
		if(flag):
			self.__exist=True
		return flag
	def Set_BorderThickness(self,thickness:int):
		'''
			设置边界厚度，为0则不设置。
			该参数用于鼠标的边界感应
		'''
		self.__borderThick=thickness
	def Set_SmoothResize(self,flag:bool):
		'''
			在设置宽高比时有效。
			如果smooth为假则矩形的宽高总是WH的整数倍，smooth为真则可以是小数倍(体现为矩形的变化是流畅不断续)
		'''
		self.__stepResizeMin.Set_Smooth(flag)
		self.__stepResizeMax.Set_Smooth(flag)
		self.Opt_Update()
	def Set_LimitArea(self,L:int,T:int,R:int,B:int):
		'''
			设置限定区域，矩形将在这个区域以内。
			准确的说是对应的边将在对应的区间之内，例如左右边界在区间[L,R]内，上下边界同理。
			允许传入有限值(即其他值为None)，以指定受限边
		'''
		opInside=self.__opInside
		opInside[0].Set_Section(L,R)
		opInside[1].Set_Section(T,B)
		self.Opt_Update()
	def Set_LimitSize(self,minSize:tuple=None,maxSize:tuple=None):
		'''
			设置限制大小，传入None将视作无限制。
			传入参数均是2-tuple，如果值是None则对应的宽/高不受限，例如传入minSize=(30,None)，则最小宽为30，高不受限
		'''
		opLimit=self.__opLimit
		minW,minH=minSize if minSize else (None,None)
		maxW,maxH=maxSize if maxSize else (None,None)
		opLimit[0].Set_MinLength(minW)
		opLimit[0].Set_MaxLength(maxW)
		opLimit[1].Set_MinLength(minH)
		opLimit[1].Set_MaxLength(maxH)
		self.Opt_Update()
	def Set_IncludingArea(self,L:int,T:int,R:int,B:int):
		'''
			设置必包含区域，矩形将一定包含这个区域。
			准确的说是对应的边将落在对应的无穷区间，例如左边界在(∞,L]，右边界在[R,∞)，上下边界同理
			允许传入有限值(即其他值为None)，以指定受限边
		'''
		raise Exception("此功能暂未实现")
	def Set_SizeRate(self,W:int,H:int):
		'''
			设置宽高比。
			如果WH任一值无效(<=0)则矩形不受限制；
		'''
		self.__stepResizeMin.Set_Rate(W,H)
		self.__stepResizeMax.Set_Rate(W,H)
		self.Opt_Update()
	def Set_Flippable(self,LR:bool,TB:bool):
		'''
			设置是否允许翻转，如果LR为假则在边界拖拽时L边界无法越过R边界，TB同理
		'''
		lst=[LR,TB]
		opFlip=self.__opFlip
		for i in range(2):
			opFlip[i].Set_Flippable(lst[i])
		self.Opt_Update()






