
import sqlite3
import time

__all__=['XJ_SQLite']

class SearchSet:#SELECT结果集
	__table=None
	__conn=None
	__col=None
	__temp='temp_{key}'
	def __init__(self,conn,tableName,conditions=[],mainKey=None):
		self.__table=tableName
		self.__conn=conn
		self.__temp=self.__temp.format(key=int(time.time()*10**6))#记录到微秒级，避免重名
		self.__DropTemp()#安全第一，先删为敬
		#SQL使用关键字DISTINCT去重：https://blog.csdn.net/weixin_46348403/article/details/120487295
		#SQL使用LIMIT跳过前n条数据：https://www.cnblogs.com/dongml/p/10953846.html
		tcols=self.__GetColsName()
		if(mainKey and mainKey in tcols):
			self.__col=mainKey
		else:
			self.__col=tcols[0]
		conditions=" AND ".join(conditions) if conditions else 'TRUE'
		cmd='CREATE TEMPORARY TABLE {tempTable} AS SELECT DISTINCT {cmpCol} FROM {table} WHERE {conditions}'
		cmd=cmd.format(tempTable=self.__temp,cmpCol=self.__col,table=tableName,conditions=conditions)
		if(self.__conn.execute(cmd)==None):
			raise Exception('SearchSet结果集创建异常——SELECT命令失败')
	def __del__(self):
		try:
			self.__DropTemp()
		except:
			pass
	def __len__(self):
		return self.Get_RowCount()
	def __DropTemp(self):
		cmd='DROP TABLE IF EXISTS {tempTable}'
		cmd=cmd.format(tempTable=self.__temp)
		self.__conn.execute(cmd)
	def __GetColsName(self):#获取列表名
		cmd='PRAGMA table_info({table})'.format(table=self.__table)
		cols=[item[1] for item in self.__conn.execute(cmd).fetchall()]
		return cols
	def Get_Rows(self,start=0,count=-1,cols=[],tableName=None):#获取指定位置和指定列的数据内容，指定table的话将内联到其他表
		if(count<0):
			count=self.Get_RowCount()
		if(not cols):
			cols=self.__GetColsName()
		if(self.__col in cols):
			cols[cols.index(self.__col)]=f'{self.__temp}.{self.__col}'
		table=tableName if tableName else self.__table
		cmd='SELECT {cols} FROM {tempTable} INNER JOIN {table} ON {tempTable}.{cmpCol}={table}.{cmpCol} LIMIT {start},{count}'
		cmd=cmd.format(tempTable=self.__temp,table=table,cmpCol=self.__col,cols=','.join(cols),start=start,count=count)
		cur=self.__conn.execute(cmd)
		return cur.fetchall()
	def Get_RowCount(self):#获取结果集大小
		cmd='SELECT COUNT(*) FROM {table}'
		cmd=cmd.format(table=self.__temp)
		cur=self.__conn.execute(cmd)
		return cur.fetchone()[0]
	def Set_SegData(self,**replaceMap):#更新当前结果集内的所有字段数据
		if(replaceMap):
			replacements=[]
			extra=[]
			for col,val in replaceMap.items():
				extra.append(bytearray(str(val).encode()))
				replacements.append(f"{col}=?")
			replacements=','.join(replacements)
			cmd='UPDATE {table} SET {replacements} WHERE {cmpCol} IN (SELECT {tempTable}.{cmpCol} FROM {tempTable} WHERE {tempTable}.{cmpCol}={table}.{cmpCol})'
			cmd=cmd.format(table=self.__table,tempTable=self.__temp,cmpCol=self.__col,replacements=replacements)
			return self.__conn.execute(cmd,extra)!=None
		return False
	def Opt_DeleteRows(self):#将结果集对应的表格数据全部删干净
		cmd='DELETE FROM {table} WHERE {cmpCol} IN (SELECT {tempTable}.{cmpCol} FROM {tempTable} WHERE {tempTable}.{cmpCol}={table}.{cmpCol})'
		cmd=cmd.format(table=self.__table,tempTable=self.__temp,cmpCol=self.__col)
		return self.__conn.execute(cmd)!=None

class ConnectionProxy:#包装Connection并记录历史execute(并且execute失败时不会抛出异常，相对的会返回None而不是Cursor对象
	__history=None
	__echo=None
	__conn=None
	__count=None
	__overflow=None
	def __init__(self,conn,count=500,echo=False):
		self.__history=[]
		self.__echo=echo
		self.__cur=conn
		self.__count=count
		self.__overflow=min(count/5,1000)
		exclude=dir(self)
		props=filter(lambda prop :prop not in exclude,dir(conn))
		props=filter(lambda prop :prop[:2]!='__' , props)
		for prop in props:
			attr=getattr(conn,prop)
			setattr(self,prop,attr)
	def Opt_ClearHistory(self):
		self.__history.clear()
	def Get_HistoryExecute(self):#获取历史执行
		return self.__history
	def execute(self,*cmd):
		cursor=None
		try:
			cursor=self.__cur.execute(*cmd)
			if(self.__echo):
				print('sql>',cmd)
		except Exception as e:
			print()
			print('sql>',cmd)
			print(e)
			print()
		if(len(self.__history)>self.__count+self.__overflow):
			self.__history=self.__history[self.__overflow:]
		self.__history.append((*cmd,cursor!=None))
		return cursor

class XJ_SQLite:
	__conn=None
	def __init__(self,sqlPath,echo=True):
		self.__conn=ConnectionProxy(sqlite3.connect(sqlPath))
	def __del__(self):
		self.__conn.close()
	def Opt_CreateTable(self,tableName,cols,force=False):#创建表格。force为真则先删后建
		if(tableName in self.Get_Tables()):
			if(force):
				self.Opt_DeleteTable(tableName)
			else:
				return
		cmd='CREATE TABLE {table} ({cols})'
		cmd=cmd.format(table=tableName,cols=",".join(cols))
		return self.__conn.execute(cmd)!=None
	def Opt_AppendRow(self,tableName,lst):#追加一条数据
		#插入blob数据：https://www.coder.work/article/4919605
		cmd='INSERT INTO {table} VALUES ({values})'
		cmd=cmd.format(table=tableName,values=','.join(['?']*len(lst)))
		return self.__conn.execute(cmd,lst)!=None
	def Opt_DeleteTable(self,tableName):#删除表格
		cmd='DROP TABLE IF EXISTS {table}'
		cmd=cmd.format(table=tableName)
		return self.__conn.execute(cmd)!=None
	def Opt_Commit(self):#提交修改
		self.__conn.commit()
	def Get_RowSearchSet(self,tableName,*conditions,mainKey=None):#搜索符合条件的数据，返回SearchSet对象
		try:
			return SearchSet(self.__conn,tableName,conditions,mainKey)
		except:
			pass
		return None
	def Get_Tables(self):#获取所有表格(名称)
		cmd='SELECT name FROM sqlite_master'
		rst=self.__conn.execute(cmd)
		return set(map(lambda item:item[0],rst.fetchall()))
	def Get_ColsName(self,tableName):#获取列表名
		#获取列名：https://geek-docs.com/sqlite/sqlite-questions/9_sqlite_how_to_get_a_list_of_column_names_on_sqlite3_database.html
		cmd='PRAGMA table_info({table})'
		cmd=cmd.format(table=tableName)
		cols=[item[1] for item in self.__conn.execute(cmd).fetchall()]
		return cols
	def Get_HistoryCommands(self):#获取历史执行
		return self.__conn.Get_HistoryExecute()
	def Opt_ClearHistory(self):#清除历史执行
		self.__conn.Opt_ClearHistory()
