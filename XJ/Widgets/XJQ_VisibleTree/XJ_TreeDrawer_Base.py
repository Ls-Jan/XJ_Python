
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_TreeDrawer_Base']

from .XJ_CoordinateTree import XJ_CoordinateTree
from typing import Tuple,List,Dict


class XJ_TreeDrawer_Base:
	'''
		基于XJ_CoordinateTree的可视树绘制器基类。
		派生类需重写：
			- _DrawLine；
			- _DrawNode；
			- _DrawStart；
			- _DrawEnd；
			- _InsertNode；
	'''
	def __init__(self):
		self.__colLine:Dict[Tuple[int,int],Tuple[int,int,int,int]]={(0,0):(0,0,0,255)}#特殊照顾(以其他颜色绘制线条)
		self.__tree:XJ_CoordinateTree=XJ_CoordinateTree()
	def Set_LineColor(self,col:Tuple[int,int,int],*links:Tuple[int,int],clear:bool=False):
		'''
			为指定的节点连线设置颜色。
			如果links为空则视为修改默认颜色(初始颜色为纯黑(0,0,0))。
			clear为真则清除之前的颜色设置。
		'''
		col=(*col,255)
		if(clear):
			self.__colLine.clear()
			self.__colLine[(0,0)]=(0,0,0)
		if(links):
			for link in links:
				if(link[0]>link[1]):
					link=(link[1],link[0])
				self.__colLine[link]=col
		else:
			self.__colLine[(0,0)]=col
		self.Opt_Update()
	def Set_NodeSize(self,nodeID:int,W:float,H:float,applyAll:bool=False):
		'''
			对指定节点设置大小。
			如果指定nodeID<0则设置默认大小(只影响后续插入节点)，
			如果applyAll为真则会对所有节点进行设置。
		'''
		if(nodeID<0 or applyAll):
			self.__tree.Set_DefaultNodeSize(W,H,applyAll)
		else:
			self.__tree.Set_NodeSize(nodeID,W,H)
	def Set_Interval(self,row:int,col:int):
		'''
			设置行列的间隔
		'''
		self.__tree.Set_Interval(row,col)
	def Opt_NodeInsert(self,nodeID:int,index:int=-1,updateImmediately:bool=True):
		'''
			插入节点，可指定是第几个子节点(默认最右)，返回节点id。
			可以指定updateImmediately以减少节点插入过程中的性能损耗(只不过节点插入完成后需手动调用Opt_Update)。
		'''
		id=self.__tree.Opt_NodeInsert(nodeID,index)
		self._InsertNode(id)
		if(updateImmediately):
			self.Opt_Update()
		return id
	def Get_NodeCount(self):
		'''
			获取节点个数
		'''
		return self.__tree.Get_NodeCount()
	def Opt_Update(self):
		'''
			更新画布
		'''
		class Node:
			posLTWH:Tuple[float,float,float,float]#节点位置(左上宽高)
			nexts:List[int]#子节点索引
		nodes:List[Node]=[]
		L,T,R,B=0,0,0,0#根节点坐标锁定(0,0)，也没什么理由去动它
		for info in self.__tree.Get_NodesGeometry():
			node=Node()
			node.posLTWH,node.nexts=info
			nodes.append(node)
			x,y,w,h=node.posLTWH
			R=max(R,x+w)
			B=max(B,y+h)
		self._DrawStart(int(R),int(B))
		for index in range(len(nodes)):
			node=nodes[index]
			x,y,w,h=node.posLTWH
			nexts=node.nexts
			self._DrawNode(x,y,w,h,index)
			if(nexts):
				node=nodes[nexts[-1]]
				y0=y+h-1
				y2=node.posLTWH[1]
				y1=(y0+y2)>>1
				xs=[]
				cols=[]
				colx=[]
				for nIndex in nexts:
					col=self.__colLine.get((index,nIndex),None)
					if(col):
						col=list(col)
						col[-1]=128#半透明
						cols.append()
						colx.append(len(xs))
					node=nodes[nIndex]
					x,y,w,h=node.posLTWH
					xs.append(x+(w>>1))
				x0=xs[0]
				col=self.__colLine[(0,0)]
				self._DrawLine(x0,y0,x0,y2,col)
				if(len(xs)>1):
					self._DrawLine(x0,y1,xs[-1],y1,col)
					for x in xs[1:]:
						self._DrawLine(x,y1,x,y2,col)
				if(cols):#存在彩线
					cols[-1][-1]=255#垫底彩色线条必不透明，其余半透明
					for x,col in reversed(zip(colx,cols)):#带颜色的，从垫底(最右)开始绘制
						self._DrawLine(x0,y0,x0,y1,col)
						self._DrawLine(x0,y1,x,y1,col)
						self._DrawLine(x,y1,x,y2,col)
		self._DrawEnd()
	def _DrawStart(self,w:int,h:int):
		'''
			绘制开始，传入的w和h为绘制大小
		'''
		pass
	def _DrawEnd(self):
		'''
			绘制结束
		'''
		pass
	def _DrawLine(self,x1:int,y1:int,x2:int,y2:int,rgba:Tuple[int,int,int,int]):
		'''
			绘制线条
		'''
		pass
	def _DrawNode(self,x:int,y:int,w:int,h:int,nodeID:int):
		'''
			绘制节点
		'''
		pass
	def _InsertNode(self,nodeID:int):
		'''
			插入新节点
		'''
		pass

