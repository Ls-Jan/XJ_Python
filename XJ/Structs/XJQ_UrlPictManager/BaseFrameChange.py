
from PyQt5.QtGui import QPixmap
from enum import Enum

class BaseFrameChange:
	'''
		回调类，子类需重写__call__函数
	'''
	class Type(Enum):
		Loading=0#请求中
		Success=1#请求成功(数据有效)
		Fail=-1#请求失败
		Invalid=-2#请求成功(无效数据)
	__pix:QPixmap=None
	__type:Type=Type.Fail
	def __call__(self,pix:QPixmap,type:Type):
		'''
			图片发生变化时的动作。
		'''
		self.__pix=pix
		self.__type=type
	def Get_Pixmap(self):
		'''
			返回图片
		'''
		return self.__pix
	def Get_Type(self):
		'''
			返回加载类型Type
		'''
		return self.__type
		
