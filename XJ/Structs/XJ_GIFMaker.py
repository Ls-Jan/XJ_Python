
__version__='1.1.0'
__author__='Ls_Jan'

from ..Functions.CV2LoadPict import *
from .XJ_Frame import *

import os
# import cv2
# import numpy as np
import ctypes
import PIL#动图类型的，cv2处理不了(或者是我没找到方法?)，只能借助PIL.Image
from threading import Thread
from io import BytesIO
# import imageio
#不用imageio这个粪，简单的gif都能给我生成好几倍的大小
#要问imageiio.mimsave的参数？可以通过imageio.help('GIF')查看，这玩意儿没法调保存质量，真是搞笑

__all__=['XJ_GIFMaker']

class XJ_GIFMaker:
	'''
		读取mp4、gif、webp、jpg、png文件为np.ndarray数据。
		可以不读取视频帧，直接指定frames以及duration以保存为gif文件。
		frames列表存放的是XJ_Frame对象。
		视频文件生成gif往往体积会增大数倍甚至数十倍，谨慎，最好先优化(例如大小调整、舍弃帧)再进行gif生成。
	'''
	__th=None#操作线程
	frames=None
	duration=None
	size=None
	def __init__(self):
		self.frames=[]
		self.size=[0,0]
		self.duration=0
	def __del__(self):
		self.Opt_ClearCache()
	def Opt_Insert(self,data,index:int=None):
		'''
			向列表中插入新的数据。
			data可以是路径(str)，也可以是图片数据(np.ndarray)。
			返回插入的数据数量
		'''
		if(isinstance(data,str)):
			path=data
			info=XJ_Frame.Get_Info(path)
			frames=[XJ_Frame(path,index) for index in range(info['count'])]
			if(self.duration==0):
				self.duration=info['duration']
		else:
			frames=[XJ_Frame(data)]
		if(not index):
			index=len(self.frames)
		for f in reversed(frames):
			self.frames.insert(index,f)
		size=frames[0].size()
		for i in range(2):
			self.size[i]=max(self.size[i],size[i])
		return len(frames)
	def Opt_SaveGif(self,
				 path:str=None,
				 index:list=[],
				 scale:int=1,
				 quality:int=85,
				 disposal:bool=False,
				 callback=lambda data:print("Finish-SavingGIF")):#保存为gif图片(bytes)
		'''
			path不为空时将图片保存到指定路径，后续调用callback时传入的data为None；
			path不指定时保存到内存，后续调用callback时传入的data为图片数据(bytes)；
			index为图片索引，可以以此调整帧的先后顺序(又或者是跳帧)；
			scale为图片缩放；
			callback为图片保存完毕后的回调函数；
			当生成的动图有“残影”效果时需指定disposal为真(disposal为假可以减少生成的gif大小)。

			特别的，如果回调函数callback为None那么以同步的方式运行。
		'''
		if(self.__th):
			print('上一次的操作仍在进行中')
			return None
		if(scale<=0):
			scale=1
		frames=self.frames.copy()
		if(len(index)):
			lenF=len(frames)
			frames=[frames[i] for i in index if 0<=i<lenF]
		if(frames):
			# frames=[PIL.Image.fromarray(f.data(size)) for f in frames]
			size=self.size
			duration=self.duration
			for i in range(len(frames)):
				f=frames[i]
				if(isinstance(f,tuple)):
					f=self.Func_LoadMP4Frame(*f)
			def Finish_Resize(frames):
				def Finish_Save(data):
					self.__th=None
					if(callback):
						callback(data)
				self.Func_SaveGIF(frames,duration,quality,disposal,path,Finish_Save)
			if(callback):
				self.__th=Thread(target=self.Func_TransFrames,args=(frames,size,Finish_Resize))
				self.__th.start()
			else:
				frames=self.Func_GetFrames(frames,size)
				return self.Func_SaveGIF(frames,duration,quality,disposal,path)
	def Get_IsBusy(self):
		'''
			获取当前操作状态
		'''
		return self.__th!=None
	def Opt_StopOperation(self):
		'''
			强制中断当前操作
		'''
		self.Func_ThreadForceStop(self.__th)
		self.__th=None
	@classmethod
	def Opt_ClearCache(self):
		XJ_Frame.Opt_ClearCache()
	@staticmethod
	def Func_TransFrames(frames,size,callback=lambda data:None):
		'''
			将XJ_Frame列表转为np.ndarray列表。
			因为图片大小调整是一件耗时任务，单独抽离出来以便丢进线程中执行
		'''
		frames=[f.data(size) for f in frames]
		callback(frames)
		return frames
	@staticmethod
	def Func_SaveGIF(
			frames,
			duration,
			quality,
			disposal=True,
			fp=None,
			callback=lambda data:None):#保存GIF
		'''
			这里主用PIL.Image.save的方式进行保存。
			frames为np.ndarray或是PIL.Image。
			
			PIL.Image.save关键参数：https://www.osgeo.cn/pillow/handbook/image-file-formats.html#gif
			PIL.Image.save保存到内存：https://blog.csdn.net/sdlypyzq/article/details/108197715
		'''
		frames=[PIL.Image.fromarray(frame) if isinstance(frame,np.ndarray) else frame for frame in frames]
		returnData=False
		if(fp==None):
			fp=BytesIO()
			returnData=True
		frames[0].save(fp,format="GIF",append_images=frames[1:],quality=quality,duration=duration,save_all=True,optimize=True,loop=0,disposal=2 if disposal else 0)
		data=None
		if(returnData):
			data=fp.getvalue()
			fp.close()
		callback(data)
		return data
	@staticmethod
	def Func_ThreadForceStop(th:Thread):#线程强制终止
		ctypes.pythonapi.PyThreadState_SetAsyncExc(th.ident, ctypes.py_object(SystemExit))

