
__version__='1.1.1'
__author__='Ls_Jan'

import os
import numpy as np
import cv2#用来处理视频
from PIL import Image#用来处理图片
from threading import Lock

class XJ_Frame:
	'''
		读取视频/图片资源并从中获取帧信息。
	'''
	__cache={}#{路径:PIL.Image对象/cv2.VideoCapture对象}
	__size={}#{路径:(宽,高)}
	__locks={}#{PIL.Image对象/cv2.VideoCapture对象:Lock线程锁}
	__path=None
	__index=None
	__data=None
	__hint=None
	def __init__(self,*data,hint:str=''):
		'''
			两种初始化方式：
				XJ_Frame(path,index=0)：文件路径，帧索引。
				XJ_Frame(data)：图片数据np.ndarray。
			hint作为辅助，用于附加额外的补充信息。后期可通过setName进行修改
		'''
		if(isinstance(data[0],np.ndarray)):
			self.__data=data[0]
		else:
			self.__path=data[0]
			self.__index=0 if len(data)==1 else data[1]
		self.__hint=hint
	def data(self,size:tuple=None,allowScale=True,fixedRate=True):
		'''
			获取帧数据，返回np.ndarray。
			size指定分辨率。
			allowScale为假时，指定分辨率若比原有的要大则不进行处理。
			fixedRate为比例缩放。
		'''
		if(self.__data):
			frame=self.__data
			if(size):
				frame=cv2.resize(frame,size)
			return frame
		path=self.__path
		index=self.__index
		isMP4=os.path.splitext(path)[1]=='.mp4'
		im=self.__cache.setdefault(path,self.CV2_LoadFile(path) if isMP4 else self.PIL_LoadFile(path))
		if(size!=None):
			oldSize=self.size()
			rate=[size[i]/oldSize[i] for i in range(2)]
			if(not allowScale):
				for i in range(2):
					if(rate[i]>1):
						rate[i]=1
			if(fixedRate):
				mRate=min(rate)
				rate=[mRate,mRate]
			size=(int(rate[i]*oldSize[i]) for i in range(2))
			size=tuple(size)
		imd=id(im)
		if(imd not in self.__locks):
			self.__locks[imd]=Lock()
		lock=self.__locks[imd]
		lock.acquire()
		frame=self.CV2_GetFrame(im,index) if isMP4 else self.PIL_GetFrame(im,index)
		lock.release()
		if(size):
			frame=cv2.resize(frame,size)
		return frame
	def size(self):
		'''
			获取初始大小
		'''
		if(self.__data):
			size=self.__data.shape[-2::-1]
		else:
			if(self.__path not in self.__size):
				self.__size[self.__path]=self.Get_Info(self.__path)['size']
			size=self.__size[self.__path]
		return size
	def path(self):
		'''
			返回文件路径
		'''
		return self.__path
	def index(self):
		'''
			返回帧索引
		'''
		return self.__index
	def hint(self):
		'''
			获取hint数据
		'''
		return self.__hint
	def setName(self,hint:str):
		'''
			设置hint数据
		'''
		self.__hint=hint
		
	@classmethod
	def Opt_ClearCache(self):
		'''
			清空缓存
		'''
		for im in self.__cache.values():
			if(isinstance(im,cv2.VideoCapture)):
				im.release()
			else:
				im.close()
		for lock in self.__locks.values():
			lock.acquire()
			lock.release()
		self.__cache.clear()
		self.__size.clear()
		self.__locks.clear()
	@classmethod
	def Get_Info(self,path:str):
		'''
			指定路径，获取视频/动画相关信息，
			返回动画信息：size、duration、count
		'''
		isMP4=os.path.splitext(path)[1]=='.mp4'
		if(isMP4):#视频用CV2读取
			fs=self.__cache.setdefault(path,self.CV2_LoadFile(path))
			info=self.CV2_GetInfo(fs)
		else:
			im=self.__cache.setdefault(path,self.PIL_LoadFile(path))
			info=self.PIL_GetInfo(im)
		return info
	@staticmethod
	def PIL_LoadFile(path:str):
		'''
			PIL.Image可以读取图片，包括静图和动图。
			返回Image对象
		'''
		im = Image.open(path)
		im.load()#调用该函数后info中的信息才会有效(这是试出来的)
		return im
	@staticmethod
	def PIL_GetInfo(im:Image.Image):
		'''
			传入PIL.Image.Image对象，
			返回动画信息：size、duration、count
		'''
		size=im.size
		count=im.n_frames if hasattr(im,'n_frames') else 1
		duration=im.info.get('duration',0)
		return {'size':size,'duration':duration,'count':count}
	@staticmethod
	def PIL_GetFrame(im:Image.Image,index:int):
		'''
			从PIL.Image.Image对象中读取帧
		'''
		size=im.size
		im.seek(index)#设置当前所在帧
		b=im.convert("RGBA").tobytes() if im.mode!="RGBA" else im.tobytes()#将所有非RGBA的全无脑转成RGBA（GIF动图的0帧往往是P模式(调色板)
		arr=np.frombuffer(b,dtype=np.uint8)
		frame=arr.reshape(size[1],size[0],4)
		return frame
	@staticmethod
	def CV2_LoadFile(path:str):
		'''
			CV2可以读取视频。
			返回cv2.VideoCapture对象
		'''
		im = cv2.VideoCapture(path)
		if(not im.isOpened()):
			raise Exception(f'文件【{path}】不存在')
			#cv2读取视频信息：https://blog.csdn.net/qq_31375855/article/details/107301118
		return im
	@staticmethod
	def CV2_GetInfo(vc:cv2.VideoCapture):
		'''
			传入cv2.VideoCapture对象，
			返回动画信息：size、duration、count
		'''
		count=vc.get(cv2.CAP_PROP_FRAME_COUNT)
		fps=vc.get(cv2.CAP_PROP_FPS)
		w=vc.get(cv2.CAP_PROP_FRAME_WIDTH)
		h=vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
		size=(w,h)
		duration=int(1000/fps)
		count=int(count)
		return {'size':size,'duration':duration,'count':count}
	@staticmethod
	def CV2_GetFrame(vc:cv2.VideoCapture,index:int):
		'''
			从cv2.VideoCapture对象中读取帧
		'''
		vc.set(cv2.CAP_PROP_POS_FRAMES,index)#设置当前所在帧
		ret, frame = vc.read()#读取帧
		frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)#opencv读取到BGR，转成RGBA
		# frame = frame[..., ::-1]#这个只能转成RGB，不如cv2自带的cvtColor函数
		return frame
	

