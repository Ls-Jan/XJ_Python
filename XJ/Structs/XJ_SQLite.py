

__version__='1.0.2'
__author__='Ls_Jan'

import sqlite3 
from typing import Union

__all__=['XJ_SQLite']
class XJ_SQLite:
	'''
		对SQLite3数据库操作进行简单的封装。
		全是单表操作。

		【新增】
			Get_RowsData支持了左连接、内连接查询功能；
			Get_RowsData支持了查询结果保存为新表功能；
	'''
	def __init__(self,sql:Union[str,sqlite3.Connection]=':memory:'):
		if(isinstance(sql,str)):
			sql=sqlite3.connect(sql)
		self.__sql=sql
	def Get_SQL(self):
		'''
			获取sqlite3.Connection数据库实例对象
		'''
		return self.__sql
	def Get_TablesName(self,temp:bool=False):
		'''
			获取所有表格(名称)，
			表格分为临时表和非临时表两种，按需查询
		'''
		table='sqlite_temp_master' if temp else 'sqlite_master'
		cmd=f'SELECT name FROM {table}'
		cur=self.__sql.execute(cmd)
		return set(map(lambda item:item[0],cur.fetchall()))	
	def Get_ColsName(self,tableName:str):
		'''
			获取指定表格的列表名
		'''
		#获取列名：https://geek-docs.com/sqlite/sqlite-questions/9_sqlite_how_to_get_a_list_of_column_names_on_sqlite3_database.html
		cmd='PRAGMA table_info({table})'
		cmd=cmd.format(table=tableName)
		cols=[item[1] for item in self.__sql.execute(cmd).fetchall()]
		return cols	
	def Set_RowsData(self,tableName:str,*conditions,**fields):
		'''
			在指定表格中搜索符合conditions中任一条件的数据，并将指定字段设置为指定内容。
			conditions和fields都必须指定，否则不处理，（想改变整个表的数据那么conditions指定为'TRUE'即可
		'''
		if(conditions and fields):
			replacements=[]
			extra=[]
			for col,val in fields.items():
				extra.append(val)
				replacements.append(f"{col}=?")
			replacements=','.join(replacements)
			conditions=" OR ".join(conditions) if conditions else 'TRUE'
			cmd='UPDATE {table} SET {replacements} WHERE {conditions}'
			cmd=cmd.format(table=tableName,replacements=replacements,conditions=conditions)
			return self.__sql.execute(cmd,extra)!=None
	def Get_RowsData(self,
					tableName:str,
					*conditions,
					conditionsLink:str='OR',
					cols:list=[],
					orderKey:str=None,
					ascend:bool=None,
					start:int=-1,
					count:int=-1,
					distinct:bool=False,
					onlyCount:bool=False,
					joinTableName:str=None,
					innerJoinCondition:str=None,
					leftJoinCondition:str=None,
					saveToNewTable:str=None,
					newTableIsTemp:bool=True):
		'''
			在指定表格中搜索符合conditions中任一条件的数据，返回匹配结果。
			通过指定onlyCount为真，可以获取匹配的数据行数。

			指定cols以获取列数据(不指定则默认全返回)。
			指定start和count以获取特定范围内的数据。
			指定distinct可以对数据进行去重。
			指定conditionsLink可以决定conditions是以哪种方式连接，默认是OR。
			额外指定ascend可以以orderKey为准进行升序降序排列(orderKey不指定则默认rowid)

			【新增】
				innerJoinCondition、LeftJoinCondition和JointTableName用于与其他表进行内连接查询，
				例如有个表Stu(id,name)和表Score(id,score)，
				可以通过Get_RowsData('Stu',cols=['Stu.name','Score.score'],joinTableName='Score',innerJoinCondition='Stu.id==Score.id')的方式查询
			【新增】
				通过指定saveToNewTable可以将查询结果另存为一张新表，不能是已有的表否则将保存失败，
				表的列名可通过cols使用AS子句设置，例如cols=['Stu.name AS stuName','Score.score AS score','Score.score<60 AS notPass']。
				保存的新表总默认为临时表，可通过newTableIsTemp设置为普通表。
				
				保存新表后该函数不会返回查询结果。
			'''
		#SQL使用LIMIT跳过前n条数据：https://www.cnblogs.com/dongml/p/10953846.html
		rank='' if ascend==None else 'ORDER BY {orderKey} {dire}'.format(orderKey=orderKey if orderKey else 'rowid',dire='ASC' if ascend else 'DESC')
		conditions=list(filter(lambda condition:condition,conditions))
		conditions=f" {conditionsLink} ".join(map(lambda val:f'({val})',conditions)) if conditions else 'TRUE'
		conditions=f'WHERE {conditions}'
		joinCondition=''
		distinct='DISTINCT' if distinct else ''
		cols='count(*)' if onlyCount else ','.join(cols if cols else self.Get_ColsName(tableName))
		if(joinTableName):
			if(leftJoinCondition):
				joinCondition=f'LEFT JOIN {joinTableName} ON {leftJoinCondition}'
			elif(innerJoinCondition):
				joinCondition=f'INNER JOIN {joinTableName} ON {innerJoinCondition}'
			else:
				pass
		if(saveToNewTable):
			if (saveToNewTable in self.Get_TablesName(True).intersection(self.Get_TablesName(False))):
				return None
			temp='TEMPORARY' if newTableIsTemp else ''
			createNewTableAs=f'CREATE {temp} TABLE {saveToNewTable} AS'
		else:
			createNewTableAs=''
		cmd='{createNewTableAs} SELECT {distinct} {cols} FROM {table} {joinCondition} {conditions} {rank} LIMIT {start},{count}'
		cmd=cmd.format(createNewTableAs=createNewTableAs,distinct=distinct,cols=cols,table=tableName,joinCondition=joinCondition,conditions=conditions,rank=rank,start=start,count=count)
		curr=self.__sql.execute(cmd)
		if(not saveToNewTable):
			rst=curr.fetchall()
			return rst[0][0] if onlyCount else rst
		else:
			return None
	def Opt_CreateTable(self,tableName:str,cols:list,force:bool=False,temp:bool=False):
		'''
			创建表格。
			force为真则先删后建。
			temp为真则创建临时表
		'''
		if(tableName in self.Get_TablesName()):
			if(force):
				self.Opt_DeleteTable(tableName)
			else:
				return False
		temp='TEMPORARY' if temp else ''
		cmd='CREATE {temp} TABLE {table} ({cols})'
		cmd=cmd.format(temp=temp,table=tableName,cols=",".join(cols))
		self.__sql.execute(cmd)
		return True
	def Opt_AppendRow(self,tableName:str,lst:list):
		'''
			追加一条/一行数据
		'''
		#插入blob数据：https://www.coder.work/article/4919605
		cmd='INSERT INTO {table} VALUES ({values})'
		cmd=cmd.format(table=tableName,values=','.join(['?']*len(lst)))
		self.__sql.execute(cmd,lst)
		return True
	def Opt_DeleteTable(self,tableName:str):
		'''
			删除表格
		'''
		cmd='DROP TABLE IF EXISTS {table}'
		cmd=cmd.format(table=tableName)
		self.__sql.execute(cmd)
		return True
	def Opt_Commit(self):
		'''
			提交修改
		'''
		self.__sql.commit()
