
__version__='1.1.0'
__author__='Ls_Jan'

import os
import numpy as np
import cv2#用来处理视频
import PIL#用来处理图片
from PIL import Image

class XJ_Frame:
	'''
		读取视频/图片资源并从中获取帧信息。
	'''
	__cache={}#{路径:大小:对象}
	__path=None
	__index=None
	__data=None
	def __init__(self,*data):
		'''
			XJ_Frame(path,index)：文件路径，帧索引。
			XJ_Frame(data)：图片数据np.ndarray
		'''
		if(len(data)==1):
			self.__data=data[0]
		else:
			self.__path=data[0]
			self.__index=data[1]
	def data(self,size:tuple=None):
		'''
			获取帧数据，返回np.ndarray。
			size指定分辨率。
		'''
		if(self.__data):
			frame=self.__data
			if(size):
				frame=cv2.resize(frame,size)
			return frame
		path=self.__path
		index=self.__index
		isMP4=os.path.splitext(path)[1]=='.mp4'
		cache=self.__cache.setdefault(path,{})
		if(isMP4):#视频用CV2读取
			if(size not in cache):
				vc=self.CV2_LoadFile(path)
				if(size!=None):
					vc.set(cv2.CAP_PROP_FRAME_WIDTH,size[0])
					vc.set(cv2.CAP_PROP_FRAME_HEIGHT,size[1])
				cache[size]=vc
			vc=cache[size]
			frame=self.CV2_GetFrame(vc,index)
		else:#图片用PIL读取
			if(size not in cache):
				im=self.PIL_LoadFile(path)
				if(size!=None):
					im=im.resize(*size)
				cache[size]=im
			im=cache[size]
			frame=self.PIL_GetFrame(im,index)
		return frame
	def size(self):
		'''
			获取大小
		'''
		return self.__data.shape[-2::-1] if self.__data else self.Get_Info(self.__path)['size']
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

	@classmethod
	def Opt_ClearCache(self):
		'''
			清空缓存
		'''
		for items in self.__cache.values():
			for im in items.values():
				if(isinstance(im,cv2.VideoCapture)):
					im.release()
				else:
					im.close()
		self.__cache.clear()
	@classmethod
	def Get_Info(self,path:str):
		'''
			指定路径，获取视频/动画相关信息，
			返回动画信息：size、duration、count
		'''
		isMP4=os.path.splitext(path)[1]=='.mp4'
		cache=self.__cache.setdefault(path,{})
		if(isMP4):#视频用CV2读取
			fs=cache.setdefault(None,self.CV2_LoadFile(path))
			info=self.CV2_GetInfo(fs)
		else:
			im=cache.setdefault(None,self.PIL_LoadFile(path))
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
		count=im.n_frames
		duration=im.info.get('duration',0)
		return {'size':size,'duration':duration,'count':count}
	@staticmethod
	def PIL_GetFrame(im:Image.Image,index:int):
		'''
			从PIL.Image.Image对象中读取帧
		'''
		size=im.size
		im.seek(index)#设置当前所在帧
		b=im.convert("RGBA").tobytes() if im.mode!="RGBA" else im.tobytes()#0帧往往是P模式(调色板)。将所有非RGBA的全无脑转成RGBA
		arr=np.frombuffer(b,dtype=np.uint8)
		frame=arr.reshape(*size,4)
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
	

