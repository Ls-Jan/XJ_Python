
__version__='1.0.1'
__author__='Ls_Jan'

class XJ_FlatTree:
	'''
		扁平树，核心是列表，可轻易序列化
		树节点结构：[value,back,curr,nexts]
	'''
	def __init__(self,data=None):
		if(data):
			self.__data=data
		else:
			self.__data=[]
			self.__CreateNode(None,0)#创建根节点
	def data(self):#返回底层数据，主用于序列化
		return self.__data
	def Is_RootNode(self,node):#判断是否根节点
		return node[2]==0
	def Get_Value(self,node):#获取节点值
		return node[0]
	def Get_RootNode(self):#获取根节点
		return self.__data[0]
	def Get_NextNode(self,node,i,strict=False):#获取第i个子节点(i为负值则获取末尾子节点)。strict为真时i若为无效正值则返回None
		if(strict and i>=len(node[3])):
			return None
		if(i<0 or i>=len(node[3])):
			i=-1
		return self.__data[node[3][i]]
	def Get_NextNodes(self,node):#返回所有子节点(使用的是生成器而非列表)
		return (self.__data[i] for i in node[3])
	def Get_NextNodeCount(self,node):#获取子节点个数
		return len(node[3])
	def Get_BackNode(self,node):#获取上级节点
		return self.__data[node[1]]
	def Get_SiblingsPst(self,node):#获取该节点在兄弟节点中的位置
		if(self.Is_RootNode(node)):
			return 0
		return self.Get_BackNode(node)[3].index(node[2])
	def Set_NodeValue(self,node,value):#设置节点值
		node[0]=value
		return True
	def Set_SiblingsPst(self,node,pst):#调整该节点在兄弟节点位置。(pst为负值则插到末尾
		if(not self.Is_RootNode(node)):
			bNode=self.Get_BackNode(node)
			bNode[3].remove(node[2])
			if(pst<0):
				bNode[3].append(node[2])
			else:
				bNode[3].insert(pst,node[2])
		return True
	def Opt_CreateNext(self,node,value,pst=-1):#创建并返回子节点。pst为第i个节点(负值则插到末尾
		nNode=self.__CreateNode(value,node[2])
		if(pst<0):
			node[3].append(nNode[2])
		else:
			node[3].insert(pst,nNode[2])
		return nNode
	def Opt_SearchNodes(self,data,key=lambda A,B:A==B):#根据key函数和data值搜索并返回所有匹配节点(使用的是生成器而非列表)
		return (node for node in self.__data if key(node[0],data))
	def Opt_RemoveNode(self,node):#移除节点(代价较大，每个节点的数据都将重新处理，慎用)。移除根节点等同于清除所有数据
		if(self.Is_RootNode(node)):
			self.__data.clear()
			self.__CreateNode(None)
			return True
		self.Get_BackNode(node)[3].remove(node[2])

		#因为该树的特殊性，越新的节点越靠后
		rmLst=[]
		stack=[node]
		while(len(stack)):
			node=stack.pop()
			rmLst.append(node[2])
			stack.extend(self.Get_NextNodes(node))
		rmLst.sort()

		#更新索引
		step=[[0,-1]]
		for index in rmLst:
			step.append([index,step[-1][1]+1])
		step.append([len(self.__data),step[-1][1]+1])
		step.pop(0)
		section=[i[0] for i in step]
		def Trans(val):
			i=0
			for s in section:
				if(val<s):
					break
				i+=1
			return val-step[i][1]
		section=set(section)
		for index in range(len(self.__data)):
			if(index in section):
				continue
			node=self.__data[index]
			node[1]=Trans(node[1])
			node[2]=Trans(node[2])
			node[3]=[Trans(i) for i in node[3]]

		#移除节点
		for pst in reversed(rmLst):
			self.__data.pop(pst)
		return True
	def __CreateNode(self,value,back):#新增节点
		node=[value,back,len(self.__data),[]]
		self.__data.append(node)
		return node


if __name__ == '__main__':

	tr=XJ_FlatTree()
	node=tr.Get_RootNode()
	node=tr.Opt_CreateNext(node,'A')
	tr.Opt_CreateNext(node,'A1')
	tr.Opt_CreateNext(node,'A2')
	node=tr.Opt_CreateNext(node,'AB')
	tr.Opt_CreateNext(node,'AB1')
	tr.Opt_CreateNext(node,'AB2')
	tr.Opt_CreateNext(node,'AB3')
	node=tr.Get_RootNode()
	tr.Opt_CreateNext(node,'X')
	node=tr.Opt_CreateNext(node,'Y')
	tr.Opt_CreateNext(node,'Y1')
	tr.Opt_CreateNext(node,'Y2')
	tr.Opt_CreateNext(node,'Y3')

	i=0
	for n in tr.data():
		print(i,n)
		i+=1
	print()

	tr.Opt_RemoveNode(list(tr.Opt_SearchNodes('AB'))[0])

	i=0
	for n in tr.data():
		print(i,n)
		i+=1
