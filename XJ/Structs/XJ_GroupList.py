
__version__='1.0.0'
__author__='Ls_Jan'

__all__=['XJ_GroupList']

class XJ_GroupList:
	'''
		能对数据简单分组的列表。
		支持多级分组。
	'''
	def __init__(self):
		self.__lst=[]
		self.__groups={}
	def __len__(self):
		return self.Get_Count()
	def Get_GroupsInfo(self):
		'''
			获取所有组的信息，返回的是字典，格式为{<str>:{'name':<str>,'count':<int>,'subGroup':{...}}}。
			不允许修改返回的字典数据。
		'''
		return self.__groups
	def Get_Count(self):
		'''
			获取列表长度
		'''
		return len(self.__lst)
	def Get_ItemData(self,index:int):
		'''
			返回指定索引的数据
		'''
		if(0<=index<len(self.__lst)):
			return self.__lst[index][0]
	def Get_ItemGroup(self,index:int,returnName:bool=True):
		'''
			获取指定索引的对应分组。
			如果returnName为真则返回对应名称列表。
		'''
		if(0<=index<len(self.__lst)):
			group=self.__lst[index][1]
			if(returnName):
				groups=self.__groups
				name=[]
				for g in group:
					groupInfo=groups[g]
					groups=groupInfo['subGroup']
					name.append(groupInfo['name'])
				group=tuple(name)
			return group
	def Get_GroupItemCount(self,group:tuple):
		'''
			获取指定组下的项数量
		'''
		groupInfo=self.__GetGroupInfo(group)
		return groupInfo['count'] if groupInfo else 0
	def Get_GroupName(self,group:tuple):
		'''
			获取指定组的组名
		'''
		groupInfo=self.__GetGroupInfo(group)
		if(groupInfo):
			return groupInfo['name']
	def Set_GroupName(self,group:tuple,name:str):
		'''
			设置指定组的组名
		'''
		groupInfo=self.__GetGroupInfo(group)
		if(groupInfo):
			groupInfo['name']=name
			return True
		return False
	def Opt_Insert(self,*datas,index:int=-1,group:tuple=tuple(),subGroup:bool=True):
		'''
			指定位置插入图片，返回图片所属的group。
			index为负数则追加到末尾。
			group为元组，形如(<str>/<int>,...)，确定分组。
			subGroup为真则在group下创建新的子组
		'''
		if(group or subGroup):
			if(subGroup):
				group=list(group)
				groups=self.__groups
				for g in group:
					groups=groups.setdefault(g,{'name':str(g),'count':0,'subGroup':{}})['subGroup']
				sub=0
				while(sub in groups):
					sub+=1
				groups.setdefault(sub,{'name':str(sub),'count':0,'subGroup':{}})
				group.append(sub)
				group=tuple(group)
			if(index<0):
				index=len(self.__lst)
			tmp=self.__lst[index:]
			del self.__lst[index:]
			self.__lst.extend([[data,group] for data in datas])
			self.__lst.extend(tmp)
			self.__UpdateGroupInfo({group:len(datas)})
			return group
	def Opt_Remove(self,*indices,start:int=0,count:int=0):
		'''
			移除指定项
		'''
		indices=sorted(set(range(start,start+count)).union(indices),reverse=True)
		count=len(self.__lst)
		while(indices[0]>=count):
			indices.pop(0)
		record={}
		for i in indices:
			item=self.__lst.pop(i)
			group=item[1]
			record.setdefault(group,0)
			record[group]-=1
		self.__UpdateGroupInfo(record)
	def __GetGroupInfo(self,group:tuple):
		'''
			返回group对应信息，为{'name':<str>,'count':<int>,'subGroup':<dict>}
		'''
		try:
			groups=self.__groups
			for g in group[:-1]:
				groups=groups[g]['subGroup']
			return groups[group[-1]]
		except:
			return None
	def __UpdateGroupInfo(self,groups:dict):
		'''
			更新组的count信息。
			如果更新后组的count为0那么将移除对应的组
		'''
		for group,count in groups.items():
			groups=self.__groups
			for g in group:
				if(g not in groups):
					break
				upper=groups
				groupInfo=groups[g]
				groupInfo['count']+=count
				if(groupInfo['count']<=0):
					upper.pop(g)
					break
				groups=groupInfo['subGroup']


