
__version__='1.1.0'
__author__='Ls_Jan'


from .XJQ_PictCarousel import XJQ_PictCarousel
from ...Functions.GetRealPath import GetRealPath
from ...Structs.XJ_GIFMaker import XJ_GIFMaker
from ...ModuleTest import XJQ_Test

from PyQt5.QtGui import QImage,QPixmap


__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		pc=XJQ_PictCarousel()
		pc.setStyleSheet('.XJQ_PictCarousel{background:#333333;}')
		# pc.setStyleSheet('.XJQ_PictCarousel{background:#222222;};QLabel{color:#FFFFFF;background:#FF0000;}')
		self.__pc=pc
	def Opt_Run(self):
		print('请选择一个动图(不选择视频是因为该操作会将所有的帧数据加载进内存，只要视频稍微大一点就容易爆内存)')
		self.__pc.show()
		self.__pc.resize(1200,700)
		file=self.Get_File(GetRealPath('../../Icons/Loading/加载动画-4.gif'),'选择一个动图',"*.png;*.jgp;*.gif;*.webp")
		if(file):
			gm=XJ_GIFMaker()
			gm.Opt_Insert(GetRealPath(file))
			frames=[QPixmap(QImage(f.data(),*gm.size, gm.size[0]*4,QImage.Format_RGBA8888)) for f in gm.frames]
			# t.Set_Duration(im.info.get('duration',50))
			self.__pc.Set_Frames(frames)
			self.__pc.Set_Duration(gm.duration)
			self.__pc.Set_Loop(50)
			self.__pc.Opt_Play(True)
		super().Opt_Run()
		return self.__pc



