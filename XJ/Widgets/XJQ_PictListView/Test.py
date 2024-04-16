
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

		lvPict=XJQ_PictListView()
		# lvPict.Opt_Insert(gm.frames,hash(file),"AAA")
		# lvPict.Opt_Insert(gm.frames,hash(file),"BBB",10)
		# lvPict.Set_VisibleGroup((hash(file),0),showAll=True)
		# lvPict.Set_VisibleGroup((hash(file),0))
		self.__lvPict=lvPict
	def Opt_Run(self):
		self.__lvPict.show()
		self.__lvPict.resize(800,400)

		print('请选择一个图片/视频进行加载')
		file=self.Get_File(GetRealPath('../../Icons/Loading/加载动画-7.gif'),'请选择一个图片/视频进行加载')
		if(file):
			print('鼠标悬停在列表中时可预览对应项的图片')
			gm=XJ_GIFMaker()
			gm.Opt_Insert(file)
			self.__lvPict.Opt_Insert(gm.frames,-1,file,groupName="AAA")
			# self.__lvPict.Opt_Insert(gm.frames,3,file,groupName="BBB")

		super().Opt_Run()
		return self.__lvPict

