
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from ...Functions.GetRealPath import GetRealPath
from .XJQ_UrlPictManager import XJQ_UrlPictManager
from .FrameChange_Label import FrameChange_Label

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from PyQt5.QtGui import QMovie,QPixmap
from PyQt5.QtCore import QSize

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		wid=QWidget()
		self.__wid=wid
	def Opt_Run(self):
		wid=self.__wid
		urls=[
			'https://github.githubassets.com/assets/mona-loading-dark-static-8b35171e5d6c.svg',
			'https://github.githubassets.com/assets/mona-loading-dark-static-8b35171e5d6c.svg',
			'https://github.githubassets.com/assets/mona-loading-dark-static-8b35171e5d6c.svg',
			GetRealPath('../../Icons/首页.png'),
			GetRealPath('../../Icons/收藏.png'),
		]
		fileLoad=GetRealPath('../../Icons/Loading/加载动画-7.gif')
		fileFail=GetRealPath('../../Icons/文件错误.png')
		mv=QMovie(fileLoad)
		sz=QSize(96,96)

		mv.setScaledSize(sz)
		wid.resize(800,400)
		wid.show()
		pm=XJQ_UrlPictManager(mv,QPixmap(fileFail).scaled(sz))
		vbox=QVBoxLayout(wid)
		for url in urls:
			lb=QLabel()
			vbox.addWidget(lb)
			pm.Opt_RequestUrl(url,FrameChange_Label(lb,sz))

		super().Opt_Run()
		return self.__wid

