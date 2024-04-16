
__version__='1.0.0'
__author__='Ls_Jan'

from ..XJQ_BaseTask import XJQ_BaseTask
from ..XJ_Frame import XJ_Frame
from ...Functions.CV2ToQPixmap import CV2ToQPixmap

__all__=['XJQ_GettingPixmapTask']
class XJQ_GettingPixmapTask(XJQ_BaseTask):
	'''
		丢进任务池的任务。
		专用于从XJ_Frame中获取对应QPixmap。
	'''
	def __init__(self,id:int,pict:XJ_Frame,size:tuple=None,allowScale=True,callback=lambda id,data:None)->None:
		'''
			id：任务id；
			pict：图片元数据，类型为XJ_Frame；
			size：要获取的图片分辨率，传入None则采用默认分辨率；
			allowScale：图片是否允许放大；
			callback：生成Qpixmap后的回调函数，接受参数为(id:int,result:QPixmap)
		'''
		super().__init__(id,callback)
		self.__pict=pict
		self.__size=size
		self.__allowScale=allowScale
	def doTask(self) -> None:
		pict=self.__pict
		pict=pict.data(self.__size,self.__allowScale)
		pict=CV2ToQPixmap(pict)
		return pict
	