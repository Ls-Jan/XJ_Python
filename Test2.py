from XJ.Widgets.XJQ_PictCarousel import *
from XJ.Functions.GetRealPath import *
from XJ.Structs.XJ_GIFMaker import *

from PyQt5.QtWidgets import QApplication,QWidget,QLabel
from PyQt5.QtGui import QImage,QPixmap,QMovie
from PyQt5.QtCore import QBuffer,QByteArray,pyqtSignal

class XJQ_GIFMovie(QLabel):
	updateMovie=pyqtSignal(bytes)
	def __init__(self):
		super().__init__()
		self.__buf=QBuffer()
		self.__mv=QMovie()
		self.__mv.setDevice(self.__buf)
		self.setMovie(self.__mv)
		self.updateMovie.connect(self.__UpdateMovie)
	def __UpdateMovie(self,data):
		mv=self.__mv
		buf=self.__buf
		buf.setData(data)
		# mv.setCacheMode(QMovie.CacheAll)#用不上
		mv.start()
		self.update()


if True:
	app = QApplication([])

	lb=Test()
	lb.show()
	lb.resize(400,400)

	file='XJ/Widgets/icons/加载动画-1.gif'
	gm=XJ_GIFMaker()
	size=gm.Opt_LoadSource(GetRealPath(file))
	gm.Opt_SaveGif(callback=lambda data:lb.updateMovie.emit(data))

	app.exec_()

