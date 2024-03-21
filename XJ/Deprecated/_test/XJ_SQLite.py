from ..XJ_SQLite import *

if True:
	sql = XJ_SQLite()
	sql.Opt_CreateTable('test',['id','name','data'])

	sql.Opt_AppendRow('test',[1,'A','a'])
	sql.Opt_AppendRow('test',[2,'A','abc'])
	sql.Opt_AppendRow('test',[5,'B',3])
	sql.Opt_AppendRow('test',[4,'B',4.56])
	sql.Opt_AppendRow('test',[3,'C',None])
	sql.Opt_AppendRow('test',[1,'D',str({1:'100'})])
	rs=sql.Get_RowSearchSet('test','name="A" AND INSTR(data,"b")')
	rs.Set_SegData(data=str({'A':"AAA",3:["1",None,3],'E':None}))
	print(list(rs.Get_Rows()))

	print('\n\n表格内容')
	print(sql.Get_RowCount('test'))
	# for i in sql.Get_RowSearchSet('test').Get_Rows():
	for i in sql.Get_RowSearchSet('test',ascend=True,orderKey='id').Get_Rows():
		print(i)
	print('\n\n历史输入')
	for i in sql.Get_HistoryCommands():
		print(f'{i[:-1]}【{i[-1]}】')

