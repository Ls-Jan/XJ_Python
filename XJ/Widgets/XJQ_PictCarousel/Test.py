
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

		file='./加载动画-4.gif'
		gm=XJ_GIFMaker()
		gm.Opt_Insert(GetRealPath(file))
		frames=[QPixmap(QImage(f.data(),*gm.size, gm.size[0]*4,QImage.Format_RGBA8888)) for f in gm.frames]

		pc=XJQ_PictCarousel()
		# t.Set_Duration(im.info.get('duration',50))
		pc.Set_Frames(frames)
		pc.Set_Duration(gm.duration)
		pc.Set_Loop(50)

		pc.setStyleSheet('.XJQ_PictCarousel{background:#333333;}')
		# pc.setStyleSheet('.XJQ_PictCarousel{background:#222222;};QLabel{color:#FFFFFF;background:#FF0000;}')
		self.__pc=pc
	def Opt_Run(self):
		self.__pc.Opt_Play(True)
		self.__pc.show()
		self.__pc.resize(1200,700)
		return super().Opt_Run()



