__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from PyQt5.QtWidgets import QWidget,QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QMovie,QPixmap
from .XJQ_UrlPict import XJQ_UrlPict,UrlPictConfig
from ...ModuleTest import XJQ_Test
from ...Functions.GetRealPath import GetRealPath

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		wid=QWidget()
		self.__wid=wid
	def Opt_Run(self):
		self.__wid.resize(640,480)
		self.__wid.show()
		urls=[
			'https://github.githubassets.com/assets/mona-loading-dark-static-8b35171e5d6c.svg',
			'https://github.githubassets.com/assets/mona-loading-dark-static-8b35171e5d6c.svg',
			'https://github.githubassets.com/assets/mona-loading-dark-static-8b35171e5d6c.svg',
			GetRealPath('./放映带#B%C&D.png'),
			GetRealPath('./放映带#B%C&D.png'),
		]
		config=UrlPictConfig((32,32),QMovie(GetRealPath('./加载动画-1.gif')),QPixmap(GetRealPath('./文件错误.png')))
		box=QVBoxLayout(self.__wid)
		for url in urls:
			print(f'异步请求图片数据：{url}')
			pict=XJQ_UrlPict(config,QUrl(url))
			box.addWidget(pict)
		super().Opt_Run()
		# return self.__wid






