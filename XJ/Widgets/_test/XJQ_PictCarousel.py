from ..XJQ_PictCarousel import *
from ...Functions.GetRealPath import *
from ...Structs.XJ_GIFMaker import *

from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QImage,QPixmap

if True:
	app = QApplication([])

	file='../icons/加载动画-1.gif'
	gm=XJ_GIFMaker()
	gm.Opt_LoadSource(GetRealPath(file),callback=None)
	frames=[QPixmap(QImage(f.data,*gm.size, gm.size[0]*4,QImage.Format_RGBA8888)) for f in gm.frames]

	pc=XJQ_PictCarousel()
	# t.Set_Duration(im.info.get('duration',50))
	pc.Set_Frames(frames)
	pc.Opt_Play(True)
	pc.Set_Duration(50)
	pc.Set_Loop(50)
	pc.show()
	pc.resize(1200,700)

	pc.setStyleSheet('.XJQ_PictCarousel{background:#333333;}')
	# pc.setStyleSheet('.XJQ_PictCarousel{background:#222222;};QLabel{color:#FFFFFF;background:#FF0000;}')

	app.exec_()

