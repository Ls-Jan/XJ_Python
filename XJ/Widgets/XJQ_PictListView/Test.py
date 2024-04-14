
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from ..XJQ_PictListView import XJQ_PictListView
from ...Structs.XJ_GIFMaker import XJ_GIFMaker
from ...Functions.GetRealPath import GetRealPath

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		file=GetRealPath('./加载动画-7.gif')
		gif=GetRealPath('./加载动画-8.gif')
		gm=XJ_GIFMaker()
		gm.Opt_Insert(file)

		lvPict=XJQ_PictListView()
		lvPict.Opt_Insert(gm.frames,-1,file,groupName="AAA")
		lvPict.Opt_Insert(gm.frames,3,file,groupName="BBB")
		lvPict.Set_LoadingGIF(gif)
		# lvPict.Opt_Insert(gm.frames,hash(file),"AAA")
		# lvPict.Opt_Insert(gm.frames,hash(file),"BBB",10)
		# lvPict.Set_VisibleGroup((hash(file),0),showAll=True)
		# lvPict.Set_VisibleGroup((hash(file),0))
		self.__lvPict=lvPict
	def Opt_Run(self):
		self.__lvPict.show()
		self.__lvPict.resize(800,400)
		return super().Opt_Run()

