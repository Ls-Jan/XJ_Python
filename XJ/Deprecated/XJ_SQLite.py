
__version__='1.0.0'
__author__='Ls_Jan'

import sqlite3
import time

__all__=['XJ_SQLite']

class SearchSet:
	'''
		SELECT结果集，本质上是创建了一个临时表，一般由XJ_SQLite.Get_RowSearchSet创建获得
	'''
	__table=None
	__conn=None
	__col=None
	__temp='temp_{key}'
	def __init__(self,conn:sqlite3.Connection,tableName:str,conditions:list=[],mainKey:str='',orderKey:str=None,ascend:bool=None):
		'''
			创建SELECT结果集，需指定键值mainKey(不指定则默认第0列为主键)。
			指定ascend可以以orderKey为准进行升序降序排列(orderKey不指定则默认mainKey)
		'''
		self.__table=tableName
		self.__conn=conn
		self.__temp=self.__temp.format(key=int(time.time()*10**6))#记录到微秒级，避免重名
		self.__DropTemp()#安全第一，先删为敬
		tcols=self.__GetColsName(self.__conn,tableName)
		if(mainKey and mainKey in tcols):
			self.__col=mainKey
		else:
			self.__col=tcols[0]
		rank=''
		conditions=" OR ".join(conditions) if conditions else 'TRUE'
		if(ascend!=None):
			rank='ORDER BY {orderKey} {dire}'
			if(orderKey==None):
				orderKey=self.__col
			dire='' if ascend==None else 'ASC' if ascend else 'DESC'
			rank=rank.format(orderKey=orderKey,dire=dire)
		#SQL使用关键字DISTINCT去重：https://blog.csdn.net/weixin_46348403/article/details/120487295
		cmd='CREATE TEMPORARY TABLE {tempTable} AS SELECT DISTINCT {cmpCol} FROM {table} WHERE {conditions} {rank}'
		cmd=cmd.format(tempTable=self.__temp,cmpCol=self.__col,table=tableName,conditions=conditions,rank=rank)
		if(self.__conn.execute(cmd)==None):
			raise Exception(f'{cmd}\nSearchSet结果集创建异常——SELECT命令失败')
	def __del__(self):
		try:
			self.__DropTemp()
		except:
			pass
	def __len__(self):
		return self.Get_RowCount()
	def __DropTemp(self):
		'''
			删除临时表
		'''
		cmd='DROP TABLE IF EXISTS {tempTable}'
		cmd=cmd.format(tempTable=self.__temp)
		self.__conn.execute(cmd)
	@staticmethod
	def __GetColsName(conn:sqlite3.Connection,tableName:str):
		'''
			获取列表名
		'''
		cmd='PRAGMA table_info({table})'.format(table=tableName)
		cols=[item[1] for item in conn.execute(cmd).fetchall()]
		return cols
	def Get_Rows(self,start=0,count=-1,*,cols=[],tableName=None,returnCount=False):
		'''
			获取指定位置和指定列的数据内容，指定table的话将内联到其他表(只不过需要存在同个主键)。
			返回的是一个生成器(实际上是Sqlite3.Cursor对象)。
			如果returnCount为真则返回数据个数
		'''
		if(not tableName):
			tableName=self.__table
		if(returnCount):
			cols='COUNT(*)'
		else:
			if(not cols):
				cols=self.__GetColsName(self.__conn,tableName)
			if(self.__col in cols):
				cols[cols.index(self.__col)]=f'{self.__temp}.{self.__col}'
			cols=','.join(cols)
		#SQL使用LIMIT跳过前n条数据：https://www.cnblogs.com/dongml/p/10953846.html
		cmd='SELECT {cols} FROM {tempTable} INNER JOIN {table} ON {tempTable}.{cmpCol}={table}.{cmpCol} LIMIT {start},{count}'
		cmd=cmd.format(tempTable=self.__temp,table=tableName,cmpCol=self.__col,cols=cols,start=start,count=count)
		cur=self.__conn.execute(cmd)
		return cur.fetchone()[0] if returnCount else cur
	def Get_Keys(self,returnCount=False):
		'''
			获取主键数据，返回的是一个生成器(实际上是Sqlite3.Cursor对象)。
			如果returnCount为真则返回主键数据个数
		'''
		if(returnCount):
			cols='COUNT(*)'
		else:
			cols=self.__col
		cmd='SELECT {cols} FROM {table}'
		cmd=cmd.format(cols=cols,table=self.__temp)
		cur=self.__conn.execute(cmd)
		return cur.fetchone()[0] if returnCount else cur
	def Set_SegData(self,tableName=None,**replaceMap):
		'''
			更新当前结果集内的所有字段数据(修改只会作用到原表)，指定table的话将设置其他表的数据
		'''
		if(replaceMap):
			if(not tableName):
				tableName=self.__table
			replacements=[]
			extra=[]
			for col,val in replaceMap.items():
				extra.append(val)
				replacements.append(f"{col}=?")
			replacements=','.join(replacements)
			cmd='UPDATE {table} SET {replacements} WHERE {cmpCol} IN (SELECT {tempTable}.{cmpCol} FROM {tempTable} WHERE {tempTable}.{cmpCol}={table}.{cmpCol})'
			cmd=cmd.format(table=tableName,tempTable=self.__temp,cmpCol=self.__col,replacements=replacements)
			return self.__conn.execute(cmd,extra)!=None
		return False
	def Opt_DeleteRows(self):
		'''
			将结果集对应的表格数据全部删干净
		'''		
		cmd='DELETE FROM {table} WHERE {cmpCol} IN (SELECT {tempTable}.{cmpCol} FROM {tempTable} WHERE {tempTable}.{cmpCol}={table}.{cmpCol})'
		cmd=cmd.format(table=self.__table,tempTable=self.__temp,cmpCol=self.__col)
		return self.__conn.execute(cmd)!=None

class ConnectionProxy:
	'''
		包装sqlite3.Connection并重写execute，以记录历史操作(execute失败时不会抛出异常，相对的会返回None而不是sqlite3.Cursor对象。
		利用了Python的动态性实现了代理效果，将sqlite3.Connection中除execute外的公开属性都直接赋值到本类创建的对象中。
	'''
	__history=None
	__echo=None
	__conn=None
	__count=None
	__overflow=None
	__print=None
	def __init__(self,conn:sqlite3.Connection,count:int=500,echo:bool=False,Print=lambda val:print(val)):
		'''
			count为记录上限。
			echo为真时每执行一个操作都将Print一次。
		'''
		self.__history=[]
		self.__echo=echo
		self.__conn=conn
		self.__count=count
		self.__overflow=min(count/5,1000)
		self.__print=Print
		exclude=dir(self)
		props=filter(lambda prop :prop not in exclude,dir(conn))
		props=filter(lambda prop :prop[:2]!='__' , props)
		for prop in props:
			attr=getattr(conn,prop)
			setattr(self,prop,attr)
	def Opt_ClearHistory(self):
		'''
			清空历史记录
		'''
		self.__history.clear()
	def Get_HistoryExecute(self):
		'''
			获取历史执行
		'''
		return self.__history
	def Get_ProxyTarget(self):
		'''
			返回代理对象，为Sqlite3.Connection对象
		'''
		return self.__conn
	def execute(self,*cmd):
		'''
			执行操作，其实就是将sqlite3.Connection.execute的操作封装了一层，
			执行失败的操作并不会抛出异常，只不过将不会返回sqlite3.Cursor对象而是返回None
		'''
		cursor=None
		try:
			cursor=self.__conn.execute(*cmd)
			if(self.__echo):
				self.__print(f'sql>{cmd}')
		except Exception as e:
			if(self.__echo):
				self.__print('')
				self.__print(f'sql>{cmd}')
				self.__print(str(e))
				self.__print('')
		if(len(self.__history)>self.__count+self.__overflow):
			self.__history=self.__history[self.__overflow:]
		self.__history.append((*cmd,cursor!=None))
		return cursor

class XJ_SQLite:
	__conn=None
	def __init__(self,sqlPath:str=':memory:',echo:bool=False):
		self.__conn=ConnectionProxy(sqlite3.connect(sqlPath),echo=echo)
	def __del__(self):
		self.__conn.close()
	def Opt_CreateTable(self,tableName:str,cols:list,force=False):
		'''
			创建表格。
			force为真则先删后建
		'''
		if(tableName in self.Get_Tables()):
			if(force):
				self.Opt_DeleteTable(tableName)
			else:
				return
		cmd='CREATE TABLE {table} ({cols})'
		cmd=cmd.format(table=tableName,cols=",".join(cols))
		return self.__conn.execute(cmd)!=None
	def Opt_AppendRow(self,tableName:str,lst:list):
		'''
			追加一条/一行数据
		'''
		#插入blob数据：https://www.coder.work/article/4919605
		cmd='INSERT INTO {table} VALUES ({values})'
		cmd=cmd.format(table=tableName,values=','.join(['?']*len(lst)))
		return self.__conn.execute(cmd,lst)!=None
	def Opt_DeleteTable(self,tableName:str):
		'''
			删除表格
		'''
		cmd='DROP TABLE IF EXISTS {table}'
		cmd=cmd.format(table=tableName)
		return self.__conn.execute(cmd)!=None
	def Opt_Commit(self):
		'''
			提交修改
		'''
		self.__conn.commit()
	def Opt_ClearHistory(self):
		'''
			清除历史执行记录
		'''
		self.__conn.Opt_ClearHistory()
	def Get_RowSearchSet(self,tableName,*conditions,mainKey:str=None,orderKey:str=None,ascend:bool=None):
		'''
			在指定表格中搜索符合conditions中任一条件的数据，返回SearchSet对象。
			
			需指定键值mainKey(不指定则默认第0列为主键)。
			额外指定ascend可以以orderKey为准进行升序降序排列(orderKey不指定则默认mainKey)
		'''
		return SearchSet(self.__conn,tableName,conditions,mainKey,orderKey,ascend)
	def Get_RowCount(self,talbeName:str):
		'''
			获取表格行数
		'''
		cmd='SELECT count(*) FROM {table}'
		cmd=cmd.format(table=talbeName)
		cur=self.__conn.execute(cmd)
		if(cur==None):
			return 0
		return cur.fetchone()[0]
	def Get_Tables(self):
		'''
			获取所有表格(名称)
		'''
		cmd='SELECT name FROM sqlite_master'
		cur=self.__conn.execute(cmd)
		return set(map(lambda item:item[0],cur.fetchall()))
	def Get_ColsName(self,tableName:str):
		'''
			获取指定表格的列表名
		'''
		#获取列名：https://geek-docs.com/sqlite/sqlite-questions/9_sqlite_how_to_get_a_list_of_column_names_on_sqlite3_database.html
		cmd='PRAGMA table_info({table})'
		cmd=cmd.format(table=tableName)
		cols=[item[1] for item in self.__conn.execute(cmd).fetchall()]
		return cols
	def Get_HistoryCommands(self):
		'''
			获取历史执行记录
		'''
		return self.__conn.Get_HistoryExecute()


