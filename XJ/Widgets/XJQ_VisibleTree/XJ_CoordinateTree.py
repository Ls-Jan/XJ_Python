
__version__='1.0.1'
__author__='Ls_Jan'
__all__=['XJ_CoordinateTree']

from typing import List
from ._Node import _Node

from typing import List

class XJ_CoordinateTree:
	'''
		简单的坐标化树，会返回节点的位置信息，隐去根节点则成为森林。
		根节点的id为0，可设置根节点坐标。
		不支持节点删除，但可以设置节点是否可见。
		每次对树进行修改后，都需要重新获取节点的值。
	'''
	__nodes:List[_Node]#所有的节点
	__nodeSize=(50,50)#节点默认大小
	__interval=(25,50)#行列之间的间隔
	__alignment:int=0#左对齐(0)、居中(1)、右对齐(-1)
	__changed:bool=False#是否发生了修改
	__reversed:bool=False#是否反向排列
	__rootPos=(0,0)#根节点坐标
	def __init__(self):
		node=_Node(*self.__nodeSize,-1)#根节点的父节点id设置为-1
		self.__nodes=[node]
	def Opt_NodeInsert(self,nodeID:int,index:int=-1):
		'''
			插入节点，可指定是第几个子节点(默认最右)，返回节点id。
		'''
		node=_Node(*self.__nodeSize,nodeID)
		if(index<0):
			index=2**30
		nodeTarget=self.__nodes[nodeID]
		nodeTarget.nodeID_children.insert(index,len(self.__nodes))
		self.__nodes.append(node)
		self.__changed=True
		return len(self.__nodes)-1
	def Opt_TreeLoad(self,nodes:List[List[int]]):
		'''
			传入数组树进行设置，其中List[int]记录的是子节点索引。
			效果等同于多次调用Opt_NodeInsert。
		'''
		self.Opt_TreeClear()
		cnt=len(self.__nodes)
		for i in range(len(nodes)):
			node=self.__nodes[i]
			node.nodeID_children=nodes[i].copy()
			for n in nodes[i]:
				while(n>=cnt):
					self.__nodes.append(_Node(*self.__nodeSize),i)
					cnt+=1
		return True
	def Opt_TreeClear(self):
		'''
			清除树，只留下根节点。
		'''
		del self.__nodes[1:]
		node=self.__nodes[0]
		node.nodeID_children.clear()
		self.__changed=True
		return True
	def Opt_NodeMove(self,nodeID_src:int,nodeID_target:int,index:int=-1):
		'''
			将目标节点(及其子节点)移动到目标节点下(作为子节点)，可指定是第几个子节点(默认最右)。
			明显的，如果target的父节点是src那么将移动失败。
		'''
		t=nodeID_target
		while(t!=-1):
			if(t==nodeID_src):
				return False
			t=self.__nodes[t].nodeID_parent
		if(index<0):
			index=2**30
		if(nodeID_src<0):
			nodeID_src=-1
		nodeSrc=self.__nodes[nodeID_src]
		nodeTarget=self.__nodes[nodeID_target]
		nodeTargetParent=self.__nodes[nodeTarget.nodeID_parent]
		nodeTargetParent.nodeID_children.remove(nodeID_target)
		nodeTarget.nodeID_parent=nodeID_src
		nodeSrc.nodeID_children.insert(index,nodeID_target)
		self.__changed=True
		return True
	def Set_NodeSize(self,nodeID:int,W:float,H:float):
		'''
			设置节点大小。
			节点高度不能过大。
		'''
		node=self.__nodes[nodeID]
		node.w=W
		node.h=H
		self.__changed=True
		return True
	def Set_NodeVisible(self,nodeID:int,flag:int):
		'''
			设置目标节点及其子节点是否可见。
			完全可见(正数)、仅隐去子节点(0)、本节点及子节点不可见(负数)。
			操作对根节点无效。
		'''
		flag=-1 if flag<0 else 0 if flag==0 else 1
		self.__nodes[nodeID].node_isVisible=flag
		self.__changed=True
		return True
	def Set_Alignment(self,flag:int):
		'''
			设置对齐，左对齐(负数)、居中(0)、右对齐(正数)。
			根节点始终是居中的
		'''
		flag=0 if flag<0 else 1 if flag==0 else -1
		old=self.__alignment
		self.__alignment=flag
		if(old!=flag):
			self.__changed=True
		return True
	def Set_DefaultNodeSize(self,W:float,H:float,applyAll:bool=False):
		'''
			设置节点默认大小，只影响后续新增节点。
			如果applyAll为真，则对所有节点进行设置。
		'''
		self.__nodeSize=(W,H)
		if(applyAll):
			for node in self.__nodes:
				node.w=W
				node.h=H
			self.__changed=True
		return True
	def Set_Interval(self,row:int,col:int):
		'''
			设置行列的间隔
		'''
		self.__interval=(row,col)
		self.__changed=True
		return True
	def Set_RootNodePos(self,x:float,y:float):
		'''
			设置根节点坐标(默认0,0)
		'''
		self.__rootPos=(x,y)
		self.__changed=True
	def Get_IsValidNodeID(self,nodeID:int):
		'''
			判断节点id是否有效。
			在使用有关节点id相关的函数之前务必确认id是否有效
		'''
		return 0<=nodeID<len(self.__nodes)
	def Get_ChildNodes(self,nodeID:int):
		'''
			获取目标节点的所有直接子节点的id。
		'''
		return self.__nodes[nodeID].nodeID_children.copy()
	def Get_NodeCount(self):
		'''
			获取当前节点个数(包括根节点在内)
		'''
		return len(self.__nodes)
	def Get_NodeGeometry(self,nodeID:int):
		'''
			获取节点左上坐标和大小，返回结果为(x,y,w,h)。
		'''
		if(self.__changed):
			self.__Opt_UpdateTree()
		node=self.__nodes[nodeID]
		return (node.x,node.y,node.w,node.h)
	def Get_NodesGeometry(self):
		'''
			获取所有节点的位置信息，返回的是一个形如[((x,y,w,h),(childID,...)),...]的列表。
		'''
		if(self.__changed):
			self.__Opt_UpdateTree()
		rst=[]
		for node in self.__nodes:
			rst.append(((node.x,node.y,node.w,node.h),node.nodeID_children.copy()))
		return rst
	def Get_Tree(self)->List[List[int]]:
		'''
			返回数组树
		'''
		return self.__nodes
	def __Opt_UpdateTree(self):
		'''
			更新整棵树。
		'''
		class Data:#一些过程变量，如果用list存的话就过于繁琐，特此结构化
			node:_Node#当前节点
			align:_Node#对齐的节点
			children:List[_Node]#未隐藏的子节点
			def __init__(self,node:_Node):
				self.node=node
				self.children=[]
				self.align=None
		width=[]#深度对应宽度
		stk=[[Data(self.__nodes[0]),],]#索引即是深度
		while(stk):#位置的确定是自底而上的，而非自顶而下。坐标是相对位置而非绝对位置
			group=stk[-1]
			if(group):#存在节点，继续向下探寻
				data=group[-1]
				if(data.node.node_isVisible==1):
					for id in data.node.nodeID_children:
						childNode=self.__nodes[id]
						if(childNode.node_isVisible!=-1):
							childNode.y=self.__nodeSize[1]+self.__interval[1]#节点高度锁定为默认值而非data.node.h
							data.children.append(childNode)
				newGroup=[Data(node) for node in data.children]
				if(self.__alignment!=1 and newGroup):
					data.align=data.children[self.__alignment]
				if(self.__reversed):
					newGroup.reverse()
				stk.append(newGroup)
			else:#子节点列表为空，反哺父节点(数据向上传递)，同时将父节点移除
				depth=len(stk)
				while(depth>=len(width)):
					width.append(-2**30)
				stk.pop()
				if(not stk):
					break
				group=stk[-1]
				data=group[-1]
				node=data.node
				align=data.align
				children=data.children
				x,w=0,0
				if(align!=None):#存在对齐
					w=align.cw
					x=align.x+w/2
					node.cw=max(align.cw,node.w)#最大列宽向上传递
				else:#无对齐，居中
					node.cw=node.w
					if(children):
						w=children[-1].x-children[0].x+children[-1].cw
						x=children[0].x+w/2
				w=max(w,node.w)
				x-=w/2#父节点理论位置(绝对位置)
				p=width[depth]+self.__interval[0]#安全位置
				x=max(x,p)#保证位置有效
				node.x=x
				width[depth]=x+node.cw+self.__interval[0]
				for d in range(depth,len(width)):#无脑更新depth后面的width
					width[d]=width[depth]
				for childNode in children:#将子节点的绝对位置重新调整为相对位置
					childNode.x=x-childNode.x
				group.pop()#该节点的数据已确定，将其移除
		if True:#处理根节点，使其居中
			node=self.__nodes[0]
			children=[self.__nodes[id] for id in data.node.nodeID_children if self.__nodes[id].node_isVisible!=-1]
			if(children):
				w=children[-1].x-children[0].x+children[-1].cw
				x=children[0].x+w/2
				node.x=x-w/2
				d=children[0].x-node.x
				for childNode in children:#重新调整子节点相对位置
					childNode.x+=d
		if True:#将根节点坐标设置为指定位置，并且将所有的节点由相对坐标改为绝对坐标
			node=self.__nodes[0]
			node.x,node.y=self.__rootPos
			stk=[node]
			while(stk):
				node=stk.pop()
				children=[self.__nodes[id] for id in node.nodeID_children if self.__nodes[id].node_isVisible!=-1]
				for childNode in children:
					childNode.x+=node.x
					childNode.y+=node.y
				stk.extend(children)
	def __Opt_PrintPos(self):
		'''
			用于Debug
		'''
		rst=[]
		for node in self.__nodes:
			rst.append(((node.x,node.y,node.w,node.h),node.nodeID_children.copy()))
		count=0
		for info in rst:
			x,y,w,h=info[0]
			print(f'{count}    {x}    {y}    {w}    {h}    ',end='')
			count+=1
			print(info[1])
		print('\n\n')


