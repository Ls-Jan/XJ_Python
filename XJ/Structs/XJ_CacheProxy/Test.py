__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

from .BaseCallback import BaseCallback
from .XJ_QUrlCacheProxy import XJ_QUrlCacheProxy
from .XJ_HttpCacheProxy import XJ_HttpCacheProxy
from ...ModuleTest import XJQ_Test

class Callback_UpdateLabel(BaseCallback):
	def __init__(self,label:QLabel):
		self.__lb=label
	def __call__(self, data: bytes,valid:bool):
		if(not valid):
			print('请求失败！')
			return False
		print('请求成功！')
		pix=QPixmap()
		pix.loadFromData(data)
		if(pix.size().isEmpty()):
			print('图片无效！')
			return False
		self.__lb.setPixmap(pix)
		print('设置成功！')
		return True


class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		wid=QLabel()
		self.__wid=wid
	def Opt_Run(self):
		self.__wid.resize(640,480)
		self.__wid.show()
		cp=XJ_QUrlCacheProxy()
		# cp=XJ_HttpCacheProxy()
		url='https://github.githubassets.com/assets/mona-loading-dark-static-8b35171e5d6c.svg'
		print(f'异步请求图片数据：{url}')
		cp.Opt_RequestUrl(url,Callback_UpdateLabel(self.__wid))
		super().Opt_Run()
		# return self.__wid






