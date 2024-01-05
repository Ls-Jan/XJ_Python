
from ..XJ_SQLite import *

if True:
	sql = XJ_SQLite(':memory:')
	sql.Opt_CreateTable('test',['id','name','data'])

	sql.Opt_AppendRow('test',[1,'A','a'])
	sql.Opt_AppendRow('test',[2,'A','abc'])
	sql.Opt_AppendRow('test',[3,'B',3])
	sql.Opt_AppendRow('test',[4,'B',4.56])
	sql.Opt_AppendRow('test',[5,'C',None])
	sql.Opt_AppendRow('test',[6,'D',str({1:'100'})])
	print(sql.Get_RowSearchSet('test','name="A"','INSTR(data,"b")').Get_Rows())
	sql.Get_RowSearchSet('test','name="A"','INSTR(data,"b")').Set_SegData(data=str({'A':"AAA",3:["1",None,3]}))
	# sql.Get_RowSearchSet('test','name="A"','INSTR(data,"b")').Set_SegData(data=str({'A':"AAA",3:["1",None,3]}))

	print('\n\n表格内容')
	for i in sql.Get_RowSearchSet('test').Get_Rows():
		print(i)
	print('\n\n历史输入')
	for i in sql.Get_HistoryCommands():
		print(i)


