
__version__='1.1.1'
__author__='Ls_Jan'

from ..Functions.CV2LoadPict import *
from .XJ_Frame import *

import ctypes
from PIL import Image#动图类型的，cv2处理不了(或者是我没找到方法?)，只能借助PIL.Image
from threading import Thread
from io import BytesIO,IOBase
# import imageio
#不用imageio这个粪，简单的gif都能给我生成好几倍的大小
#要问imageiio.mimsave的参数？可以通过imageio.help('GIF')查看，这玩意儿没法调保存质量，真是搞笑

__all__=['XJ_GIFMaker']

class XJ_GIFMaker:
	'''
		读取mp4、gif、webp、jpg、png文件为np.ndarray数据。
		可以不读取视频帧，直接指定frames以及duration以保存为gif文件。
		frames列表存放的是XJ_Frame对象。
		duration为毫秒级。
		视频文件生成gif往往体积会增大数倍甚至数十倍，谨慎，最好先优化(例如大小调整、舍弃帧)再进行gif生成。
	'''
	__th=None#操作线程
	__fp=None#BytesIO对象
	__gifSize=None#上一次保存GIF的大小
	__memSize=None#上一次保存GIF时图片的总大小
	frames=None
	duration=None
	size=None
	def __init__(self):
		self.frames=[]
		self.size=[0,0]
		self.duration=0
		self.__fp=None
		self.__gifSize=0
	def __del__(self):
		self.Opt_ClearCache()
	def Opt_Insert(self,data,index:int=None):
		'''
			向列表中插入新的数据。
			data可以是路径(str)，也可以是图片数据(np.ndarray)。
			返回插入的数据数量。

			补充：如果插入的数据数量大于1，那么插入的每个XJ_Frame的hint字符串数据会赋值为对应索引值
		'''
		if(isinstance(data,str)):
			path=data
			info=XJ_Frame.Get_Info(path)
			if(info['count']>1):
				frames=[XJ_Frame(path,index,hint=str(index)) for index in range(info['count'])]
			else:
				frames=[XJ_Frame(path)]
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
				 disposal:bool=True,
				 callback=lambda data:print("Finish-SavingGIF")):#保存为gif图片(bytes)
		'''	
			结合frames、duration、size这几个数据以及函数参数进行GIF生成；
			如果回调函数callback不为空那么将单独启动一个线程进行GIF生成；

			path不为空时将图片保存到指定路径，否则将保存到内存；
			index为图片索引，可以以此调整帧的先后顺序(又或者是跳帧)，如果index为空那么将默认为range(len(frames))；
			scale为图片缩放；
			callback为GIF生成完毕后的回调函数；
			当生成的动图有“残影”效果时需指定disposal为真(disposal为假可以减少生成的gif大小)。

			补充：
				当保存到内存时，callback为空则返回图片文件数据，否则调用callback并传入图片文件数据；
				当保存到路径时，callback为空返回None，否则调用callback并传入None；
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
			size=tuple((int(scale*self.size[i]) for i in range(2)))
			duration=self.duration
			for i in range(len(frames)):
				f=frames[i]
				if(isinstance(f,tuple)):
					f=self.Func_LoadMP4Frame(*f)
			def Finish_Save(data):
				if(path):
					self.__gifSize=os.path.getsize(path)
				else:
					data=self.__fp.getvalue()
					self.__gifSize=len(data)
					self.__th=None
					self.__fp.close()
					callback(data)
			self.__gifSize=0
			fp=open(path,'wb') if path else BytesIO()
			if(callback):
				self.__th=Thread(target=self.__Func_SaveGIF,args=(frames,duration,quality,size,disposal,fp,Finish_Save))
				self.__th.start()
			else:
				data=self.__Func_SaveGIF(frames,duration,quality,size,disposal,fp,None)
				if(path):
					self.__gifSize=os.path.getsize(path)
				else:
					self.__gifSize=len(data)
				fp.close()
				return data
		else:
			if(callback):
				callback(None)
			return None
	def Get_IsBusy(self):
		'''
			获取当前操作状态
		'''
		return self.__th!=None
	def Get_MemorySize(self):
		'''
			获取最近一次保存时占用内存的最大大小
		'''
		return self.__memSize
	def Get_SavingSize(self):
		'''
			获取最近一次保存的图片数据大小(字节)。
			当通过Opt_SaveGIF使用多线程保存GIF时可以通过该函数实时获取图片的字节大小。
		'''
		try:
			size=self.__fp.getbuffer().nbytes
		except:
			size=self.__gifSize
		return size
	def Opt_StopOperation(self):
		'''
			强制中断当前操作
		'''
		if(self.__th):
			self.Func_ThreadForceStop(self.__th)
			self.__th=None
	def Opt_Clear(self):
		'''
			清空数据
		'''
		self.frames.clear()
		self.size=[0,0]
		self.duration=0
	def __Func_SaveGIF(self,*args):
		'''
			Func_SaveGIF函数的一层过渡，
			主要用于确定列表的图片大小
		'''
		args=list(args)
		frames=args[0]
		fp=args[5]
		callback=args[6]
		resolution=args[3]
		self.__memSize=0
		for i in range(len(frames)):
			frame=frames[i]
			if(isinstance(frame,np.ndarray)):
				frame=Image.fromarray(frame)
			elif(isinstance(frame,XJ_Frame)):
				frame=Image.fromarray(frame.data(resolution,False))
			elif(isinstance(frame,Image)):
				frame=frame
			else:
				pass
			size=len(frame.tobytes())#简单测试了下，它的损耗忽略不计，应该就是内存数据
			self.__memSize+=size
		if(callback):
			self.__fp=fp
		return self.Func_SaveGIF(*args)
	@classmethod
	def Opt_ClearCache(self):
		XJ_Frame.Opt_ClearCache()
	@staticmethod
	def Func_SaveGIF(
			frames:list,
			duration:int,
			quality:int,
			resolution:tuple=None,
			disposal:int=True,
			fp:IOBase=None,
			callback=lambda data:None):#保存GIF
		'''
			这里主用PIL.Image.save的方式进行保存。
			frames为np.ndarray或是PIL.Image亦或是XJ_Frame。
			fp除了是BytesIO对象外还可以是字符串。

			PIL.Image.save关键参数：https://www.osgeo.cn/pillow/handbook/image-file-formats.html#gif
			PIL.Image.save保存到内存：https://blog.csdn.net/sdlypyzq/article/details/108197715
		'''
		frames=[Image.fromarray(frame) if isinstance(frame,np.ndarray) else Image.fromarray(frame.data(resolution,False)) if isinstance(frame,XJ_Frame) else frame for frame in frames]
		if(resolution!=None):
			resolution=tuple(resolution)
			for i in range(len(frames)):
				frame=frames[i]
				if(frame.size!=resolution):
					frames[i]=frame.resize(resolution)
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

