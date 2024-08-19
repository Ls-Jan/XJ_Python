#TODO：2024/8/18



__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_UrlPict']

import os
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QMimeData,Qt,QUrl,QByteArray
from PyQt5.QtGui import QDrag
from XJ.Structs.XJ_MouseStatus import XJ_MouseStatus
from .Config import Config
from .UpdateLabel import UpdateLabel




class XJQ_UrlPict(QLabel):
	def __init__(self,config:Config,url:QUrl,data:QByteArray=None,timeout:float=0):
		'''
			传入的url会经过一次处理以保证顺利得到数据，因此以XJQ_UrlPict.Get_Url返回的url为准。

			如果已经有图片二进制数据(内存数据/bytes)，那么传入的data的hash值将决定url(因为url要作为标识id使用)，
			此时url格式为：hash:XXXXXXX
		'''
		self.__selected=False
		self.__valid=[]
		if(data):
			url=f'hash:{hash(data)}'
			config.cacheProxy.Set_UrlData(url,data.data())
		self.setMovie(config.pictWait)
		if(url):
			if(True):#以弯弯绕的方式将本地文件路径改为用“file”前缀的url
				path=QByteArray.fromPercentEncoding(QByteArray((url.url().encode()))).data().decode()#因为QUrl会将百分号进行转义，这一步不能跳
				if(os.path.exists(path)):
					url=QByteArray(path.encode()).toPercentEncoding().data().decode()#将路径改为百分号编码
					url=QUrl(f'file:///{url}')
				url=url.url()
			cb=UpdateLabel(self,config.pictFail,self.__valid,UpdateLabel.Get_ShrinkedSize)
			config.cacheProxy.Opt_GetUrl(url,cb,timeout)
		else:
			self.setPixmap(config.pictFail)
		self.__url=url if url else ''



