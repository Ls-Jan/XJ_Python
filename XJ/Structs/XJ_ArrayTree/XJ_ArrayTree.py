
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJ_ArrayTree']

from typing import List,Dict,Tuple,Set,Type,Callable

class XJ_ArrayTree(list):
	'''
		简单的数组树，第0个元素是根节点。
		节点类型为List[int](以及派生类)，其中第0个元素为父节点索引(-1为无效索引，即父节点不存在)，其余为子节点索引。

		允许逻辑成环，但会记录重合点位置
	'''
	__invalid:List[Tuple[int,int]]#无效点位置
	__coincident:Dict[int,List[Tuple[int,int]]]#汇集点/重合点位置
	__detached:Set[int]#游离节点索引
	def __init__(self,newNode:Callable[[int],List[int]]=lambda index:[-1]):
		self.__invalid=[]
		self.__coincident={}
		self.__detached=set()
		self.__newNode=newNode
		self.append(newNode(0))
	def Get_CoincidentNodes(self):
		'''
			获取重合点位置。
			返回的Tuple[int,int]间接记录目标点，第一个值是父节点，第二个值为索引。
		'''
		return list(self.__coincident.items())
	def Get_InvalidNodes(self):
		'''
			获取无效点位置(索引对应节点不存在)。
			返回的Tuple[int,int]间接记录目标点，第一个值是父节点，第二个值为索引。
		'''
		return self.__invalid
	def Get_DetachedNodes(self):
		'''
			获取游离点(不与根节点有任何联系)索引。
		'''
		return self.__detached
	def Get_NodeCount(self):
		'''
			获取节点个数(实际是返回len(tree))
		'''
		return len(self)
	def Get_IndexIsExist(self,index:int):
		'''
			判断索引是否有效(实际是返回0<=index<len(tree))
		'''
		return 0<=index<len(self)
	def Get_NodeChild(self,index:int):
		'''
			获取子节点索引列表(实际是返回tree[index][1:])
		'''
		return self[index][1:]
	def Get_NodeParent(self,index:int):
		'''
			获取父节点索引(实际是返回tree[index][0])
		'''
		return self[index][0]
	def Opt_Update(self):
		'''
			在数据发生变动后都需要进行手动更新。
			会更新每个节点的父索引。
		'''
		self.__coincident.clear()
		self.__invalid.clear()
		self.__detached.clear()
		length=len(self)
		if(length==0):
			return False
		self.__detached=set(range(1,length))
		stk=[0]
		while(stk):
			i=stk.pop()
			j=0
			children=self[i][:0:-1]#倒序(已去除父索引)，以便深度遍历
			for n in children:
				j+=1
				if(n>=length):
					self.__invalid.append((i,j))
				else:
					c=self[n]
					if(len(c)==0):
						c.append(-1)
					c[0]=i#设置父索引
					stk.append(n)
					self.__detached.discard(n)
				self.__coincident.setdefault(n,[]).append((i,j))
		key=[]
		for i in self.__detached:
			for n in self[i][1:]:
				if(n>=length):
					self.__invalid.append((i,j))
				else:
					c=self[n]
					if(len(c)==0):
						c.append(-1)
					c[0]=i#设置父索引
		for i in self.__coincident:
			lst=self.__coincident[i]
			if(len(lst)==1):
				key.append(i)
			else:
				lst.reverse()
		for k in key:
			self.__coincident.pop(k)
		return True
	def Opt_TreeClear(self):
		'''
			清除树，只留下根节点。
		'''
		del self[1:]
		del self[0][1:]
		return True
	def Opt_NodeNewChild(self,index_target:int,index_child:int=-1,pos:int=-1):
		'''
			在目标节点的子节点列表指定位置中插入index_child。
			如果index_child为负值则自动创建新节点(节点类型已在初始化时确定)。
			返回子节点。
		'''
		length=len(self)
		if(index_target<length):
			if(pos<0):
				pos=2**30
			if(index_child<0):
				index_child=length
				node=self.__newNode(index_child)
				self.append(node)
			self[index_target].insert(pos+1,index_child)
			return self[index_child]
		return None
	def Opt_NodeMove(self,index_src:int,index_target:int,pos:int=-1):
		'''
			在进行该操作前务必调用Opt_Update进行更新。
			将src节点移动到target节点下，可指定是第几个子节点(默认最右)。
			明显的，如果src是target的父节点那么将移动失败。
			如果节点不存在也将移动失败。
		'''
		t=index_target
		length=len(self)
		if(index_src>=length):#不处理节点不存在的情况
			return False
		if(index_src==0):#不移动根节点
			return False
		while(t>0):#避免src移至src子节点下(要这么做也不是不行，就是没什么意义，搞出一堆游离点并没有什么好处)
			if(t==index_src or t>=length):
				return False
			t=self[t][0]
		if(pos<0):
			pos=2**30
		nodeSrc=self[index_src]
		nodeTarget=self[index_target]
		index_parent=[item[0] for item in self.__coincident.get(index_src,[nodeSrc[0],-1])]
		for p in index_parent:
			if(0<=p<length):
				i=self[p].index(nodeSrc,1)
				if(i>0):
					self[p].pop(i)
		nodeSrc[0]=index_target
		nodeTarget.insert(pos,index_src)
		return True

