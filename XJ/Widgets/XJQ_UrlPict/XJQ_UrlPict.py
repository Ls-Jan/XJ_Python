__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_UrlPict']

import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl,QByteArray,pyqtSignal,QBuffer
from .UrlPictConfig import UrlPictConfig
from .UpdateLabel import UpdateLabel
from ..XJQ_AutoSizeLabel import XJQ_AutoSizeLabel
from typing import Union

class XJQ_UrlPict(XJQ_AutoSizeLabel):
	loaded=pyqtSignal(bool)
	def __init__(self,config:UrlPictConfig,url:QUrl,data:Union[bytes,QPixmap]=None,timeout:float=0,func_shrinkedSize=None):
		'''
			传入的url会经过一次处理以保证顺利得到数据，因此以XJQ_UrlPict.Get_Url返回的url为准。
			func_shrinkedSize(QSize)用于图片大小的额外调整，以避免出现图片过大的情况，传入None则使用默认调整。
			加载成功/失败时会触发loaded(bool)信号，传入的布尔值代表是否成功加载，说实话这信号没啥用，自己把握罢。
			目前仅处理静图。

			如果已经有图片文件的二进制数据(bytes)，那么传入的data的hash值将决定url(因为url要作为标识id使用)，
			此时url格式为：hash:XXXXXXX
		'''
		super().__init__()
		self.__valid=[]
		if(data):
			if(isinstance(data,QPixmap)):
				arr=QByteArray()
				data.save(QBuffer(arr),'png')
				data=arr.data()
			url=f'hash:{hash(data)}'
			config.cacheProxy.Set_UrlData(url,data)
		self.setMovie(config.pictWait)
		if(url):
			if(isinstance(url,QUrl)):#以弯弯绕的方式将本地文件路径改为用“file”前缀的url
				path=QByteArray.fromPercentEncoding(QByteArray((url.url().encode()))).data().decode()#因为QUrl会将百分号进行转义，这一步不能跳
				if(os.path.exists(path)):
					url=QByteArray(path.encode()).toPercentEncoding().data().decode()#将路径改为百分号编码
					url=QUrl(f'file:///{url}')
				url=url.url()
			cb=UpdateLabel(self,config.pictFail,self.__valid,func_shrinkedSize if func_shrinkedSize else UpdateLabel.Get_ShrinkedSize)
			config.cacheProxy.Opt_RequestUrl(url,cb,timeout)
		else:
			url=''
			self.setPixmap(config.pictFail)
		self.__url:str=url
		self.__config=config
	def setPixmap(self,pix:QPixmap):
		super().setPixmap(pix)
		self.loaded.emit(self.Get_IsValid())
	def Get_Url(self):
		'''
			获取图片的url数据(str)
		'''
		return self.__url
	def Get_Pixmap(self,returnBytes:bool=False):
		'''
			获取图片数据，
			如果指定returnBytes为真则返回图片文件数据bytes(图片格式还需自个儿额外判断，麻烦)，
			否则返回QPixmap
		'''
		data=self.__config.cacheProxy.Get_UrlData(self.__url)
		if(returnBytes):
			returnBytes
		pix=QPixmap()
		pix.loadFromData(data)
		return pix
	def Get_IsValid(self):
		'''
			判断当前数据是否有效
		'''
		return bool(self.__valid)

