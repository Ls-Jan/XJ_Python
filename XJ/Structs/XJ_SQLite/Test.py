__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from ...Functions.GetRealPath import GetRealPath
from .XJ_SQLite import XJ_SQLite 

__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		# sql=XJ_SQLite('../data/LeetCode.db')
		# rst=sql.Get_TablesName()
		# rst=sql.Get_ColsName('list')
		# rst=sql.Get_ColsName('question')
		# print(rst)

		sql=XJ_SQLite()
		sql.Opt_CreateTable("Test",['name','id'])
		sql.Opt_AppendRow("Test",["A",1])
		sql.Opt_AppendRow("Test",["B",2])
		sql.Opt_AppendRow("Test",["C",3])
		sql.Opt_AppendRow("Test",[False,4])
		sql.Opt_AppendRow("Test",[True,5])
		sql.Set_RowsData("Test","id==2",**{'name':str({1:100}),'id':100})

		sql.Opt_CreateTable("ABC",['a','b','c','id'],temp=True)
		sql.Opt_AppendRow("ABC",[3,2,1,4])
		# cmd='SELECT Test.name,Test.id,ABC.a IS NOT NULL FROM Test LEFT JOIN ABC ON ABC.id==Test.id'

		# rst=sql.Get_RowsData("Test","name==True",cols=['name'])
		rst=sql.Get_RowsData("Test",cols=['Test.name','Test.id','ABC.id IS NOT NULL'],joinTableName="ABC",leftJoinCondition="ABC.id==Test.id")
		# rst=sql.Get_RowsData("Test",cols=['Test.name','Test.id','ABC.id'],joinTableName="ABC",innerJoinCondition="ABC.id==Test.id")
		# rst=sql.Get_RowsData("Test",cols=['Test.name','Test.id','ABC.id'],joinTableName="ABC",innerJoinCondition="ABC.id==Test.id",saveToNewTable='DEF')
		# rst=sql.Get_RowsData("Test",joinTableName="ABC",innerJoinCondition="ABC.c==Test.id")
		# rst=sql.Get_RowsData("Test",cols=['Test.name AS name','Test.id AS ID','ABC.c as C'],joinTableName="ABC",innerJoinCondition="ABC.c==Test.id")

		# rst=sql.Get_RowsData("Test",joinTableName="ABC",innerJoinCondition="ABC.c==Test.id",onlyCount=True)
		# rst=sql.Get_RowsData("Test")
		# rst=sql.Get_TablesName(temp=True)
		# rst=sql.Get_ColsName('DDD')
		print(rst)
		return super().Opt_Run()

