
from ..XJQ_PictListView import *
from ...Structs.XJ_Frame import *
from ...Structs.XJ_GIFMaker import *
from ...Structs.XJQ_PictLoader import *
from ...Functions.GetRealPath import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

if True:
	app = QApplication([])

	file=GetRealPath('../../Icons/Loading/加载动画-7.gif')
	gm=XJ_GIFMaker()
	gm.Opt_Insert(file)

	lvPict=XJQ_PictListView()
	lvPict.Opt_Insert(gm.frames,file,"AAA")
	lvPict.Opt_Insert(gm.frames,file,"BBB",10)
	# lvPict.Set_LoadingGIF('XJ/Icons/loading/加载动画-4.gif')
	lvPict.Set_LoadingGIF('XJ/Icons/loading/加载动画-8.gif')
	# lvPict.Set_LoadingGIF('XJ/Icons/loading/加载动画-7.gif')
	# lvPict.Opt_Insert(gm.frames,hash(file),"AAA")
	# lvPict.Opt_Insert(gm.frames,hash(file),"BBB",10)
	# lvPict.Set_VisibleGroup((hash(file),0),showAll=True)
	# lvPict.Set_VisibleGroup((hash(file),0))
	lvPict.show()
	lvPict.resize(800,400)

	app.exec_()
	exit()

