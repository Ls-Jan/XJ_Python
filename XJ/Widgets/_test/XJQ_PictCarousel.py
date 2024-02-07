from ..XJQ_PictCarousel import *
from ...Functions.GetRealPath import *
from ...Structs.XJ_GIFMaker import *

from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QImage,QPixmap

if True:
	app = QApplication([])

	file='../icons/加载动画-1.gif'
	gm=XJ_GIFMaker()
	size=gm.Opt_LoadSource(GetRealPath(file))
	frames=[QPixmap(QImage(f.data,*size, size[0]*4,QImage.Format_RGBA8888)) for f in gm.frames]

	t=XJQ_PictCarousel()
	# t.Set_Duration(im.info.get('duration',50))
	t.Set_Frames(frames)
	t.Opt_Play(True)
	t.Set_Duration(50)
	t.Set_Loop(50)
	t.show()
	t.resize(1200,700)

	# t.setStyleSheet('background:#222222;')

	app.exec_()

