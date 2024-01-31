
class XJ_RectResize:
	'''
		将矩形大小调整的逻辑抽象出来作为本类
		不使用Qt相关模块是为了足够的抽象(抽象至算法以便用于其他场合)
	'''
	
	def __init__(self):
		#关于单词flippable是否合规的探讨：https://english.stackexchange.com/questions/518696
		self.__thick=(50,)*4#边界厚度
		self.__activeBorder=[]#活跃边对应索引
		self.__pos=(0,0)#鼠标坐标
		self.__anchor=(0,0)#点击坐标(作为锚点)
		self.__rect=[0,0,0,0]#左上右下
		self.__rectD=[0,0,0,0]#拖拽后的矩形
		self.__limitSize=[(300,600),(200,400)]#限制大小(依次是宽高的最小最大值对)
		# self.__limitSize=[(None,None),(None,None)]#限制大小(依次是宽高的最小最大值对)
		self.__limitArea=[100,150,None,None]#限制区域(左上右下)
		# self.__limitArea=[None,None,None,None]#限制区域(左上右下)
		self.__limitRate=[0,0]#限制宽高比
		self.__limitRate=[1,1]#限制宽高比
		self.__smoothDrag=False#丝滑拖拽，在指定宽高比时有效
		self.__flippable=[True,True]#允许翻转(即左比右大、上比下大)，依次是X和Y
	def Opt_SetClickPos(self,pos,innerFirst=False):#设置点击位置
		'''
			innerFirst为真时，若鼠标在矩形内部区域中，无论鼠标位置多靠近边界，边界都不会选中
		'''
		self.__anchor=pos
		self.__activeBorder=self.__GetActiveBorder(self.__rect,pos,self.__thick,innerFirst)
		# print(">>>",pos,self.__activeBorder)
	def Opt_SetDragPos(self,pos):#设置鼠标拖拽位置(仅需传入鼠标位置)
		self.__pos=pos
		anchor=self.__anchor
		# rect=self.__rect.copy()
		rect=self.__rect.copy()
		active=self.__activeBorder
		for b in self.__activeBorder:
			rect[b]+=pos[b%2]-anchor[b%2]

		# print("1>>>",rect)
		# rect=self.__GetLimitRect(
		# 		rect,
		# 		self.__activeBorder,
		# 		self.__limitArea,
		# 		self.__limitRate,
		# 		self.__limitSize,
		# 		False,
		# 		# True,
		# 		True)
		# print("2>>>",rect)
		# rect=self.__GetLimitRect_Rate(rect,self.__limitRate,self.__activeBorder,True,True)
		rect=self.__GetLimitRect_Rate(rect,self.__limitRate,self.__activeBorder,False,True)
		rect=self.__GetLimitRect_Area(rect,self.__activeBorder,self.__limitArea,len(self.__activeBorder)==4)
		# rect=self.__GetLimitRect_Area(rect,self.__limitArea,len(self.__activeBorder)==4)
		rect=self.__GetLimitRect_Rate(rect,self.__limitRate,self.__activeBorder,True,True)
		# rect=self.__GetLimitRect_Area(rect,self.__limitArea,True)
		# print(rect)
		# print()
		# rect=self.__GetLimitRect_Size(rect,self.__limitSize,self.__limitRate,self.__activeBorder,self.__flippable,self.__smoothDrag)
		# rect=self.__GetSupposedRect(rect,self.__limitArea,self.__limitSize,self.__activeBorder,self.__flippable)
		# print(rect)
		self.__rectD=rect
	def Opt_MoveCancel(self):#撤销移动(本质上是将鼠标移回到最初点击位置)
		self.Opt_SetDragPos(self.__anchor)
	def Get_Rect(self,normalize=False):#返回矩形。normalize为真时调整大小关系(例如左比右大时调换左右值)
		return self.__rectD if not normalize else self.__GetNormalizeRect(self.__rectD)
	def Get_ActiveBorder(self):#获取活跃边
		'''
			'LTRB'中的任一或二或四或零字符，
			对应10种情况：
				4：L、T、R、B
				4：LT、LB、RT、RB
				1：LTRB
				1：(空字符串)
		'''
	def Set_Rect(self,rect=None,normalize=False):#设置矩形(4-list)，顺序是左上右下
		if(rect==None):
			rect=self.__rectD
		if(normalize):
			rect=self.__GetNormalizeRect(rect)
		self.__rect=rect
		self.__rectD=self.__rect.copy()
		self.__activeBorder=''
	def Set_BorderThick(self,*thick):#设置边界厚度，用于探测。顺序依次是左上右下
		if(len(thick)==1):
			thick=thick*4
		elif(len(thick)==2):
			thick=tuple([thick[i%2] for i in range(4)])
		else:
			raise Exception('Parameter-Error:',*thick)
		self.__thick=thick
	def Set_LimitSize(self,minW=None,maxW=None,minH=None,maxH=None):#设置限制大小，传入无效值(大小非正数、最小值大于最大值)将视作无限制
		lst=[[minW,maxW],[minH,maxH]]
		for i in range(2):
			item=lst[i]
			flag=0
			for j in range(2):
				val=item[j]
				if(val!=None and val>0):
					flag+=1
				else:
					val=None
				item[j]=val
			if(flag==2):
				if(item[0]>item[1]):
					item=[None,None]
			self.__limitSize[i]=tuple(item)
	def Set_LimitArea(self,area=None):#设置受限区域，以限制矩形位置。顺序是左上右下
		self.__limitArea=self.__GetNormalizeRect(area)
	def Set_SizeRate(self,W,H):#设置宽高比
		self.__limitRate=(W,H)
	def Set_Flippable(self,*,X=None,Y=None):#设置可否翻转，人话就是左边界能否超出右边界之类的
		if(X!=None):
			self.__flippable[0]=X
		if(Y!=None):
			self.__flippable[1]=Y

	@classmethod
	def __IsRectIncludePos(self,rect,pos):
		for i in range(2):
			if(not self.__IsSectionIncludeVal(rect[i::2],pos[i])):
				return False
		return True
	@classmethod
	def __IsSectionIncludeVal(self,section,val):
		return (section[0]<=val)^(section[1]<=val)
	@classmethod
	def __GetActiveBorder(self,rect,pos,thick,innerFirst=True):
		rect_Outer=rect.copy()
		rect_Inner=rect.copy()
		for i in range(2):
			sign=1 if rect[i]<rect[i+2] else -1
			rect_Outer[i]-=sign*thick[i]/2
			rect_Inner[i]=rect_Outer[i]+sign*thick[i]
			rect_Outer[i+2]+=sign*thick[i+2]/2
			rect_Inner[i+2]=rect_Outer[i+2]-sign*thick[i]
		inner_1=self.__IsRectIncludePos(rect_Outer,pos)
		inner_2=self.__IsRectIncludePos(rect_Inner,pos)
		if(inner_1):#范围内
			if(inner_2):#内部
				return [0,1,2,3]
			else:#边界
				pass
		else:#范围外
			return []
		active=[]
		border='LTRB'
		diff=[abs(pos[i%2]-rect[i]) for i in range(4)]
		flagXY=[0,0]
		for i in range(4):
			b=''
			if(diff[i]<=thick[i]/2):
				b=border[i]
				flagXY[i%2]+=1
			active.append(b)
		for i in range(2):#当边界过于靠近时以最近边为准
			if(flagXY[i]>1):
				a,b=i,i+2
				if(diff[a]<diff[b]):
					active[b]=''
				else:
					active[a]=''
		active=''.join(active)
		if(active=='' or innerFirst):
			if(self.__IsRectIncludePos(rect,pos)):
				active=border
		return [border.index(a) for a in active]
	@classmethod
	def __GetNormalizeRect(self,rect):
		rect=list(rect)
		for index in [(0,2),(1,3)]:
			a,b=index
			if(rect[a]>rect[b]):
				rect[a],rect[b]=rect[b],rect[a]
		return rect
	@classmethod
	def __GetLimitRectddd(self,rect,activeBorder,limitArea,limitRate,limitSize,forceLimitArea,smooth):
		rect=rect.copy()
		rSize=[rect[i+2]-rect[i]+1 for i in range(2)]
		aSize=[abs(rSize[i]) for i in range(2)]

		anchor=[0,0,0,0]#不动边
		weight=[0,0]
		for i in activeBorder:
			i=(i+2)%4
			anchor[i]=1

		limitSize=limitSize.copy()
		for i in range(2):
			a=limitArea[i]
			b=limitArea[i+2]
			item=list(limitSize[i])
			if(a!=None and b!=None):
				areaS=b-a
				maxS=item[0]
				if(maxS!=None and maxS<areaS):
					item[0]=areaS
			limitSize[i]=item

		# if(len(activeBorder)==1):
			# i=activeBorder[0]%2+1
			# maxS=limitSize[i][1]
			# if(maxS):
			# 	aSize[i]=maxS

		#根据limitRate调整大小
		rateW,rateH=limitRate
		if(rateW>0 and rateH>0):
			W,H=aSize
			rW,rH=W/rateW,H/rateH
			if(len(activeBorder)==1):
				rate=rW if activeBorder[0]%2==0 else rH
			else:
				rate=min(rW,rH)
			if(not smooth):
				rate=int(rate)
			W=rate*rateW
			H=rate*rateH
			aSize[0]=W if rSize[0]>0 else -W
			aSize[1]=H if rSize[1]>0 else -H

		for i in range(2):
			rect[i+2]=rect[i]+aSize[i]

		#范围约束
		for i in range(4):
			a=rect[i]
			minA=limitArea[i%2]
			maxA=limitArea[i%2+2]
			if(minA!=None and a<minA):
				a=minA
			if(maxA!=None and a>maxA):
				a=maxA
			diff=a-rect[i]
			rect[i]=a
			if(diff>0 and anchor[i]):
				rect[(i+2)%4]+=diff
		# for i in range(2):
		# 	minS=
		# 	maxS

		return rect

		# for i in range(2):
		# 	pa,pb=active[i],active[i+2]
		# 	w=0 if pa==0 else 2 if pb==0 else 1
		# 	weight[i]=w
		# 	# anchor[i]=rect[i]+w*rSize[i]/2

		for i in range(2):
			rect[i]=anchor[i]-weight[i]*aSize[i]/2
			rect[i+2]=rect[i]+aSize[i]
		return rect

		rSize=[rect[i+2]-rect[i]+1 for i in range(2)]
		aSize=[abs(rSize[i]) for i in range(2)]
		rateW,rateH=limitRate
		#根据limitSize优先扩大
		for i in range(2):
			minA=limitSize[i][0]
			if(minA!=None):
				aSize[i]=max(minA,aSize[i])
		#根据activeBorder扩大aSize对应值

		if(rateW>0 and rateH>0):
			W,H=aSize
			rW,rH=W/rateW,H/rateH
			if(len(activeBorder)==1):
				rate=rW if activeBorder[0] in [0,2] else rH
			else:
				rate=max(rW,rH)
			if(not smooth):
				rate=int(rate)
			W=rate*rateW
			H=rate*rateH
			aSize[0]=W
			aSize[1]=H
		#根据limitArea和wholeMove调整anchor以及缩小aSize
		for i in range(2):
			minA,maxA=limitArea[i],limitArea[i+2]
			a=anchor[i]
			p=aSize[i]/2
			move=False
			if(minA!=None):
				w1=weight[i]
				p1=w1*p
				if(a-p1<minA):
					if(forceLimitArea or a<minA):#脱离范围，采取整体移动
						a=minA+p1
						move=True
					else:#正常情况
						p=min(a-minA,w1*p1)/w1
			if(maxA!=None):
				w2=2-weight[i]
				p2=w2*p
				if(a+p2>maxA):
					if(forceLimitArea or a>maxA):#脱离范围，采取整体移动
						if(move):#属于二次脱离，强制缩小
							p=maxA-minA
							p2=w2*p
						a=maxA-p2+1
					else:#正常情况
						p=min(maxA-a+1,w2*p2)/w2
			aSize[i]=p*2+1
			anchor[i]=a

		#根据limitSize进行缩小aSize
		for i in range(2):
			maxA=limitSize[i][1]
			if(maxA!=None):
				aSize[i]=min(maxA,aSize[i])

		#根据limitRate缩小aSize
		rateW,rateH=limitRate
		if(rateW>0 and rateH>0):
			W,H=aSize
			rW,rH=W/rateW,H/rateH
			rate=min(rW,rH)
			if(not smooth):
				rate=int(rate)
			W=rate*rateW
			H=rate*rateH
			aSize[0]=W if rSize[0]>0 else -W
			aSize[1]=H if rSize[1]>0 else -H

		for i in range(2):
			rect[i]=anchor[i]-weight[i]*aSize[i]/2
			rect[i+2]=rect[i]+aSize[i]
		return rect

	# @classmethod
	# def __GetLimitRect(self,rect,activeBorder,limitArea,limitRate,limitSize,wholeMove,smooth):

	@classmethod
	def __GetLimitRectsss(self,rect,activeBorder,limitArea,limitRate,limitSize,wholeMove,smooth):
		rect=rect.copy()
		rSize=[rect[i+2]-rect[i]+1 for i in range(2)]
		aSize=[abs(rSize[i]) for i in range(2)]
		weight=[0,0]
		anchor=[0,0]

		#根据activeBorder确定weight和anchor
		active=[1,1,1,1]#拖拽一角则调整对应两边，拖拽一边则两侧同时调整
		for i in activeBorder:
			if(active[i]):
				active[(i+2)%4]=0
			active[i]=1
		for i in range(2):
			pa,pb=active[i],active[i+2]
			w=0 if pa==0 else 2 if pb==0 else 1
			weight[i]=w
			anchor[i]=rect[i]+w*rSize[i]/2

		#根据limitSize优先扩大
		for i in range(2):
			minA=limitSize[i][0]
			if(minA!=None):
				aSize[i]=max(minA,aSize[i])

		#根据limitRate优先扩大aSize
		rateW,rateH=limitRate
		if(rateW>0 and rateH>0):
			W,H=aSize
			rW,rH=W/rateW,H/rateH
			if(len(activeBorder)==1):
				rate=rW if activeBorder[0] in [0,2] else rH
			else:
				rate=max(rW,rH)
			if(not smooth):
				rate=int(rate)
			W=rate*rateW
			H=rate*rateH
			aSize[0]=W
			aSize[1]=H

		#根据limitArea和wholeMove调整anchor以及缩小aSize
		for i in range(2):
			minA,maxA=limitArea[i],limitArea[i+2]
			a=anchor[i]
			p=aSize[i]/2
			move=False
			if(minA!=None):
				w1=weight[i]
				p1=w1*p
				if(a-p1<minA):
					if(wholeMove or a<minA):#脱离范围，采取整体移动
						a=minA+p1
						move=True
					else:#正常情况
						p=min(a-minA,w1*p1)/w1
			if(maxA!=None):
				w2=2-weight[i]
				p2=w2*p
				if(a+p2>maxA):
					if(wholeMove or a>maxA):#脱离范围，采取整体移动
						if(move):#属于二次脱离，强制缩小
							p=maxA-minA
							p2=w2*p
						a=maxA-p2+1
					else:#正常情况
						p=min(maxA-a+1,w2*p2)/w2
			aSize[i]=p*2+1
			anchor[i]=a

		#根据limitSize进行缩小aSize
		for i in range(2):
			maxA=limitSize[i][1]
			if(maxA!=None):
				aSize[i]=min(maxA,aSize[i])

		#根据limitRate缩小aSize
		rateW,rateH=limitRate
		if(rateW>0 and rateH>0):
			W,H=aSize
			rW,rH=W/rateW,H/rateH
			rate=min(rW,rH)
			if(not smooth):
				rate=int(rate)
			W=rate*rateW
			H=rate*rateH
			aSize[0]=W if rSize[0]>0 else -W
			aSize[1]=H if rSize[1]>0 else -H

		for i in range(2):
			rect[i]=anchor[i]-weight[i]*aSize[i]/2
			rect[i+2]=rect[i]+aSize[i]
		return rect

	def __GetLimitRecteeeee(self,rect,activeBorder,limitArea,limitRate,limitSize,wholeMove,smooth):
		rect=rect.copy()
		rSize=[rect[i+2]-rect[i]+1 for i in range(2)]
		aSize=[abs(rSize[i]) for i in range(2)]
		weight=[0,0]
		anchor=[0,0]

		#根据activeBorder确定weight和anchor
		active=[1,1,1,1]#拖拽一角则调整对应两边，拖拽一边则两侧同时调整
		for i in activeBorder:
			if(active[i]):
				active[(i+2)%4]=0
			active[i]=1
		for i in range(2):
			pa,pb=active[i],active[i+2]
			w=0 if pa==0 else 2 if pb==0 else 1
			weight[i]=w
			anchor[i]=rect[i]+w*rSize[i]/2

		#根据limitSize优先扩大
		for i in range(2):
			minA=limitSize[i][0]
			if(minA!=None):
				aSize[i]=max(minA,aSize[i])

		#根据limitRate优先扩大aSize
		rateW,rateH=limitRate
		if(rateW>0 and rateH>0):
			W,H=aSize
			rW,rH=W/rateW,H/rateH
			if(len(activeBorder)==1):
				rate=rW if activeBorder[0] in [0,2] else rH
			else:
				rate=max(rW,rH)
			if(not smooth):
				rate=int(rate)
			W=rate*rateW
			H=rate*rateH
			aSize[0]=W
			aSize[1]=H

		#根据limitArea和wholeMove调整anchor以及缩小aSize
		for i in range(2):
			minA,maxA=limitArea[i],limitArea[i+2]
			a=anchor[i]
			p=aSize[i]/2
			move=False
			if(minA!=None):
				w1=weight[i]
				p1=w1*p
				if(a-p1<minA):
					if(wholeMove or a<minA):#脱离范围，采取整体移动
						a=minA+p1
						move=True
					else:#正常情况
						p=min(a-minA,w1*p1)/w1
			if(maxA!=None):
				w2=2-weight[i]
				p2=w2*p
				if(a+p2>maxA):
					if(wholeMove or a>maxA):#脱离范围，采取整体移动
						if(move):#属于二次脱离，强制缩小
							p=maxA-minA
							p2=w2*p
						a=maxA-p2+1
					else:#正常情况
						p=min(maxA-a+1,w2*p2)/w2
			aSize[i]=p*2+1
			anchor[i]=a

		#根据limitSize进行缩小aSize
		for i in range(2):
			maxA=limitSize[i][1]
			if(maxA!=None):
				aSize[i]=min(maxA,aSize[i])

		#根据limitRate缩小aSize
		rateW,rateH=limitRate
		if(rateW>0 and rateH>0):
			W,H=aSize
			rW,rH=W/rateW,H/rateH
			rate=min(rW,rH)
			if(not smooth):
				rate=int(rate)
			W=rate*rateW
			H=rate*rateH
			aSize[0]=W if rSize[0]>0 else -W
			aSize[1]=H if rSize[1]>0 else -H

		for i in range(2):
			rect[i]=anchor[i]-weight[i]*aSize[i]/2
			rect[i+2]=rect[i]+aSize[i]
		return rect

	@classmethod
	def __GetLimitRect_Rate(self,rect,limitRate,activeBorder,shrink=True,smooth=True):#获取设置宽高比后的矩形
		rect=rect.copy()
		rSize=[rect[i+2]-rect[i]+1 for i in range(2)]
		aSize=rSize.copy()
		rateW,rateH=limitRate
		if(rateW>0 and rateH>0):
			W,H=aSize
			aW,aH=abs(W),abs(H)
			rW,rH=aW/rateW,aH/rateH
			if(shrink):
				rate=min(rW,rH)
			else:
				# if(len(activeBorder)>1):
				if(len(activeBorder)!=1):
					rate=max(rW,rH)
				else:
					rate=rW if activeBorder[0]%2==0 else rH
			if(not smooth):
				rate=int(rate)
			W=rate*rateW
			H=rate*rateH
			aSize[0]=W if aSize[0]>0 else -W
			aSize[1]=H if aSize[1]>0 else -H

		if(sum((rSize!=aSize[i] for i in range(2)))):#大小发生变化
			active=[1,1,1,1]#拖拽一角则调整对应两边，拖拽一边则两侧同时调整
			for i in activeBorder:
				if(active[i]):
					active[(i+2)%4]=0
				active[i]=1
			for i in range(2):
				pa,pb=active[i],active[i+2]
				ps=pa+pb
				ra=pa/ps
				c=rect[i]+rSize[i]*ra#找锚点
				a=c-aSize[i]*ra
				rect[i]=a
				rect[i+2]=a+aSize[i]-1
		return rect
	@classmethod
	def __GetLimitRect_Area(self,rect,activeBorder,limitArea,wholeMove):#将矩形约束到范围内
		rect=rect.copy()
		# flagXY=[1,1] if wholeMove else [0,0]
		# for i in range(4):
		# 	a,b=limitArea[i%2],limitArea[i%2+2]
		# 	r=rect[i]
		# 	d=0
		# 	if(a!=None and r<a):
		# 		d=a-r
		# 		r=a
		# 	elif(b!=None and r>b):
		# 		d=b-r
		# 		r=b
		# 	rect[i]=r
		# 	if(flagXY[i%2]>0):
		# 		rect[(i+2)%4]+=d
		# 		flagXY[i%2]-=1

		rSize=[rect[i+2]-rect[i]+1 for i in range(2)]
		aSize=rSize.copy()
		weight=[0,0]
		anchor=[0,0]

		#根据activeBorder确定weight和anchor
		active=[1,1,1,1]#拖拽一角则调整对应两边，拖拽一边则两侧同时调整
		for i in activeBorder:
			if(active[i]):
				active[(i+2)%4]=0
			active[i]=1
		for i in range(2):
			pa,pb=active[i],active[i+2]
			w=0 if pa==0 else 2 if pb==0 else 1
			weight[i]=w
			anchor[i]=rect[i]+w*rSize[i]/2


		#根据limitArea和wholeMove调整anchor以及缩小aSize
		for i in range(2):
			minA,maxA=limitArea[i],limitArea[i+2]
			a=anchor[i]
			p=aSize[i]/2
			move=False
			if(minA!=None):
				w1=weight[i]
				p1=w1*p
				if(a-p1<minA):
					if(wholeMove or a<minA):#脱离范围，采取整体移动
						a=minA+p1
						move=True
					else:#正常情况
						p=min(a-minA,w1*p1)/w1
			if(maxA!=None):
				w2=2-weight[i]
				p2=w2*p
				if(a+p2>maxA):
					if(wholeMove or a>maxA):#脱离范围，采取整体移动
						if(move):#属于二次脱离，强制缩小
							p=maxA-minA
							p2=w2*p
						# a=maxA-p2
						a=maxA-p2+1
					else:#正常情况
						p=min(maxA-a+1,w2*p2)/w2
			# aSize[i]=p*2
			aSize[i]=p*2+1
			anchor[i]=a

		for i in range(2):
			rect[i]=anchor[i]-aSize[i]*weight[i]/2
			rect[i+2]=rect[i]+aSize[i]-1
		return rect

		return rect
	@classmethod
	def __GetLimitRect_Size(self,rect,limitSize,limitRate,activeBorder,flippable,smooth=False):#将矩形缩小到合适大小
		rect=rect.copy()
		rSize=[rect[i+2]-rect[i]+1 for i in range(2)]
		aSize=rSize.copy()
		for i in range(2):
			minS=limitSize[i][0]
			maxS=limitSize[i][1]
			valS=abs(aSize[i])
			sign=1 if aSize[i]>0 else -1
			if(sign<0 and not flippable[i]):
				valS=1
				sign=1
			if(minS>0 and valS<minS):
				valS=minS
			if(maxS>0 and valS>maxS):
				valS=maxS
			aSize[i]=valS if sign>0 else -valS
		return self.__GetLimitRect_Rate(rect,limitRate,activeBorder,True,smooth)
		# rateW,rateH=limitRate
		# if(rateW>0 and rateH>0):
		# 	W,H=aSize
		# 	rate=min(abs(W)/rateW,abs(H)/rateH)
		# 	if(not smooth):
		# 		rate=int(rate)
		# 	W=rate*rateW
		# 	H=rate*rateH
		# 	aSize[0]=W if aSize[0]>0 else -W
		# 	aSize[1]=H if aSize[1]>0 else -H

		# if(sum((rSize!=aSize[i] for i in range(2)))):#大小发生变化
		# 	active=[1,1,1,1]#拖拽一角则调整对应两边，拖拽一边则两侧同时调整
		# 	for i in activeBorder:
		# 		if(active[i]):
		# 			active[(i+2)%4]=0
		# 		active[i]=1
		# 	for i in range(2):
		# 		pa,pb=active[i],active[i+2]
		# 		ps=pa+pb
		# 		ra=pa/ps
		# 		c=rect[i]+rSize[i]*ra#找锚点
		# 		a=c-aSize[i]*ra
		# 		rect[i]=a
		# 		rect[i+2]=a+aSize[i]
		return rect




from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Test(QWidget):
	def __init__(self):
		super().__init__()
		self.__rs=XJ_RectResize()
		# self.__rs.Set_Rect([200,200,100,100])
		self.__rs.Set_Rect([100,100,200,200])
		# self.setMouseTracking(True)
	def paintEvent(self,event):
		# LTRB=[100,100,200,200]
		LTRB=self.__rs.Get_Rect()
		print(">>>",LTRB)
		ptr=QPainter(self)
		pen=QPen()
		pen.setWidth(50)
		ptr.setPen(pen)
		ptr.drawRect(QRect(QPoint(*LTRB[:2]),QPoint(*LTRB[2:])))
	def mouseMoveEvent(self,event):
		pos=event.pos()
		pos=(pos.x(),pos.y())
		# self.__rs.Opt_SetClickPos(pos)
		self.__rs.Opt_SetDragPos(pos)
		self.update()
		# print(pos)
		# print(self.__rs.Get_ActiveBorder())
	def mousePressEvent(self,event):
		pos=event.pos()
		pos=(pos.x(),pos.y())
		self.__rs.Set_Rect()
		self.__rs.Opt_SetClickPos(pos)
		# ab=self.__rs.Get_ActiveBorder()

if True:
	app = QApplication([])

	t=Test()
	t.show()
	t.resize(1200,700)

	app.exec_()
