
__version__='1.0.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_VisibleTree import XJQ_VisibleTree

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		vt=XJQ_VisibleTree()
		# vt.Set_NodeSize(-1,50,50,True)
		# vt.Set_Interval(25,50)
		self.__vt=vt
	def Opt_Run(self):
		vt=self.__vt
		for id in [0,1,2,3,3,5,2,5,8,7]:#指定节点下插入节点
			id=vt.Opt_NodeInsert(id,updateImmediately=False)
		for id in range(vt.Get_NodeCount()):
			node=vt.Get_Node(id)
			node.setText(str(id))
			node.clicked.connect((lambda id:lambda:print("CLICK>",id))(id))
		vt.Get_Canvas().setGeometry(600,100,1000,800)
		vt.Opt_Update()

		super().Opt_Run()
		return self.__ts




