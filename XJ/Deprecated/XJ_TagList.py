
__version__='1.0.0'
__author__='Ls_Jan'

import sqlite3

__all__=['XJ_TagList']

class XJ_TagList:
	'''
		带有tags值的列表结构。
		用于小规模数据，数据量100w以上时单次操作上升到秒级
		
		会使用sqlite3数据库创建一个表格table，列名为[rowIndex,tag,...]，
		rowIndex记录行索引，以此保证列表的顺序性，
		tag在初始化时指定的tagList确定。
	'''
	def __init__(self,table:str='Record',repository=':memory:',tagList=['default']):
		'''
			会使用sqlite3数据库创建一个表格table，列名为[rowIndex,tag,...]，
			参数tagList指定了tag的名称，如果tagList有多个数据那么表格将会创建多个tag列
		'''
		sql=sqlite3.connect(repository)
		cur=sql.execute(f'SELECT * FROM sqlite_master WHERE name=="{table}"')
		if(len(cur.fetchall())==0):
			sql.execute(f'CREATE TABLE {table} (rowIndex,{",".join(tagList)})')
		count=sql.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
		self.__count=count
		self.__sql=sql
		self.__table=table
		self.__tags=tuple(tagList)
	def Set_RowTags(self,*indices,**tagValue):
		'''
			设置某行的tag值。
			用法示例：lst.Opt_SetData(3,4,5,group=4,tag=7)，将索引3,4,5对应项的group值设置为4以及tag值设置为7
		'''
		lst=[]
		for tag,value in tagValue.items():
			if(tag in self.__tags):
				lst.append(f'{tag}={value}')
		if(lst and indices):
			self.__sql.execute(f'UPDATE {self.__table} SET {",".join(lst)} WHERE rowIndex IN ({",".join(indices)})')
	def Get_Length(self,**tagValue)->int:
		'''
			获取列表长度。
			如果指定tagValue那么将返回经过筛选后的列表长度
		'''
		if(tagValue):
			if(set(tagValue).intersection(self.__tags)):
				cur=self.__sql.execute(f'SELECT COUNT(*) FROM {self.__table} WHERE {" AND ".join([f"{tag}={tagValue[tag]}" for tag in tagValue])}')
				return cur.fetchone()[0]
			else:
				return 0
		else:
			return self.__count
	def Get_RowTags(self,start:int=0,count:int=-1,*tags)->dict:
		'''
			获取指定行的tag值，可以指定tag列，不指定则全部返回。
			如果count为负值则取值为列表长度
			返回格式为{<str>:[<int>,...]}
		'''
		tags=[tag for tag in tags if tag in self.__tags]
		if(not tags):
			tags=self.__tags
		if(start<0):
			start=0
		if(count<0):
			count=self.__count
		tempTable=f'__tempTable_{self.__table}'
		cur=self.__sql.execute(f'SELECT * FROM sqlite_master WHERE name=="{tempTable}"')
		if(len(cur.fetchall())>0):
			self.__sql.execute(f'DROP TABLE {tempTable}')
		self.__sql.execute(f'CREATE TEMPORARY TABLE {tempTable} AS SELECT {",".join(tags)} FROM {self.__table} WHERE rowIndex>={start} AND rowIndex<{start+count}')
		rst={}
		for tag in tags:
			cur=self.__sql.execute(f'SELECT {tag} FROM {tempTable} GROUP BY {tag}')
			rst[tag]=cur.fetchall()
		return rst
	def Get_SQL(self)->sqlite3.Connection:
		'''
			返回sqlite3.Connection对象。
			一般作debug使用
		'''
		return self.__sql
	def Opt_Insert(self,index=-1,count=1,**tagValue):
		'''
			插入一批重复数据，如果index为负数则追加到末尾。
			未指定的tag将默认赋值0。
			插入的位置越前，操作的代价就越大，因为需要对索引值重新进行改动
		'''
		if(count>0):
			if(index<0):
				index=self.__count
			self.__count+=count
			self.__sql.execute(f'UPDATE {self.__table} SET rowIndex=rowIndex+{count} WHERE rowIndex>={index} ')
			values=[tagValue[tag] if tag in tagValue else 0 for tag in self.__tags]

			step=1000
			loop=count//step
			pattern=f',{",".join(map(lambda key:str(key),values))}),('
			def Execute(index,step):#一次性插入大量数据
				values=''
				for j in range(index,index+step):
					values+=str(j)+pattern
				index+=step
				values='('+values[:-2]
				self.__sql.execute(f'INSERT INTO {self.__table} VALUES {values}')
			for i in range(loop):
				Execute(index,step)
				index+=step
			count=count%step
			if(count):
				Execute(index,count)
			self.__sql.commit()
	def Opt_Delete(self,start:int,count:int=1):
		'''
			删除多行数据，start如果无效则不删除数据。
			删除的代价比较大，因为需要对索引值重新进行改动
		'''
		if(count>0):
			if(0<=start<self.__count):
				count=min(start+count,self.__count)-start
				self.__sql.execute(f'DELETE FROM {self.__table} WHERE rowIndex>={start} AND rowIndex<{start+count}')
				self.__sql.execute(f'UPDATE {self.__table} SET rowIndex=rowIndex-{count} WHERE rowIndex>={start} ')
				self.__count-=count

