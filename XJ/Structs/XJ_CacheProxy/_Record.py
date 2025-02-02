__author__='Ls_Jan'
__version__='1.0.0'
__all__=['_Record']

from typing import List
from .BaseCallback import BaseCallback
from time import time

class _Record:
	'''
		结构体，存储基本数据
	'''
	def __init__(self):
		self.cbs:List[BaseCallback]=[]#BaseCallback回调对象
		self.time=time()#时间戳
		self.data=b''#数据
		self.valid=False#数据是否有效
