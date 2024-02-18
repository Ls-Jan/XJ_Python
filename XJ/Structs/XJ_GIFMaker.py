
__version__='1.0.0'
__author__='Ls_Jan'

import os
import cv2
import numpy as np
import ctypes
from PIL import Image#动图类型的，cv2处理不了(或者是我没找到方法?)，只能借助PIL.Image
from threading import Thread
from io import BytesIO
# import imageio
#不用imageio这个粪，简单的gif都能给我生成好几倍的大小
#要问imageiio.mimsave的参数？可以通过imageio.help('GIF')查看，这玩意儿没法调保存质量，真是搞笑

__all__=['XJ_GIFMaker']
class XJ_GIFMaker:
	'''
		读取mp4、gif、webp文件为np.ndarray数据
		可以不读取视频帧，指定frames以及duration以保存为gif文件
		策略是读取全部帧并加载进内存，所以不能处理过大的文件
		视频文件生成gif往往体积会增大数倍甚至数十倍，谨慎
	'''
	__maxSize=128#处理256MB的文件，不建议修改，处理过大的文件对内存而言是巨大的考验
	__th=None#保存线程
	frames=[]
	duration=50
	def __init__(self):
		self.frames=[]
	def Get_IsSaving(self):
		return self.__th!=None
	def Opt_LoadSource(self,path):#读取资源，并返回资源分辨率
		if(os.path.getsize(path)>self.__maxSize*pow(2,20)):
			print(f"文件过大，超过{self.__maxSize}MB")
			return (0,0)
		sType=os.path.splitext(path)[1]
		if(sType=='.mp4'):#视频资源
			data=self.Func_LoadMP4(path)
		elif(sType in ['.webp','.gif']):
			data=self.Func_LoadGIF(path)
		self.frames=data['frames']
		self.duration=data['duration']
		return data['size']
	def Opt_SaveGif(self,path=None,index=[],scale=1,quality=85,disposal=False,callback=lambda data:print("Finish-SavingGIF")):#保存为gif图片(bytes)
		'''
			path不为空时将图片保存到指定路径，后续调用callback时传入的data为None
			path不指定时保存到内存，后续调用callback时传入的data为图片数据(bytes)
			index为图片索引，可以以此调整帧的先后顺序(又或者是跳帧)
			callback为图片保存完毕后的回调函数
			当生成的动图有“残影”效果时需指定disposal为真(disposal为假可以减少生成的gif大小)
		'''
		frames=self.frames
		if(len(index)):
			lenF=len(frames)
			frames=[frames[i] for i in index if 0<=i<lenF]
		if(scale!=1):
			frames=[Image.fromarray(cv2.resize(f,(0,0),fx=scale,fy=scale)) for f in frames]
		if(frames):
			def Finish(data):
				self.__th=None
				callback(data)
			self.__th=Thread(target=self.Func_SaveGIF,args=(frames,self.duration,quality,disposal,path,Finish))
			self.__th.start()
	def Opt_StopSaving(self):
		self.Func_ThreadForceStop(self.__th)
		self.__th=None
	@staticmethod
	def Func_LoadGIF(path):#读取动图(包括webp)，返回frames、size、duration
		im = Image.open(path)
		im.load()#调用该函数后info中的信息才会有效(这是试出来的)
		frames=[]
		size=im.size
		duration=im.info.get('duration',50)
		for i in range(im.n_frames):
			im.seek(i)
			if(im.mode!="RGBA"):#0帧往往是P模式(调色板)。将所有非RGBA的全无脑转成RGBA
				b=im.convert("RGBA").tobytes()
			else:
				b=im.tobytes()
			arr=np.frombuffer(b,dtype=np.uint8)
			try:
				frame=arr.reshape(*size,4)
				frames.append(frame)
			except Exception as e:
				print(e)
				pass
		return {'frames':frames,'size':size,'duration':int(duration)}
	@staticmethod
	def Func_LoadMP4(path):#读取MP4文件，返回frames、size、duration
		frames=[]
		size=(0,0)
		duration=50
		video_cap = cv2.VideoCapture(path)
		# video_cap.set(cv2.CAP_PROP_POS_FRAMES,30)#设置当前所在帧，但没什么作用
		try:
			if(video_cap.isOpened()):
				#cv2读取视频信息：https://blog.csdn.net/qq_31375855/article/details/107301118
				fps=video_cap.get(cv2.CAP_PROP_FPS)
				w=video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
				h=video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
				size=(w,h)
				duration=1000/fps
				while True:
					ret, frame = video_cap.read()
					if ret is False:
						break
					frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)#opencv读取BGR，转成RGBA
					# frame = frame[..., ::-1]#这个只是转成RGB罢了
					frames.append(frame)
		except Exception as e:
			frames.pop()
			print(e)
		video_cap.release()
		return {'frames':frames,'size':size,'duration':int(duration)}
	@staticmethod
	def Func_SaveGIF(frames,duration,quality,disposal=True,fp=None,callback=lambda data:None):#保存GIF，frames为np.ndarray或是PIL.Image
		#这里主用PIL.Image.save的方式进行保存
		#PIL.Image.save关键参数：https://www.osgeo.cn/pillow/handbook/image-file-formats.html#gif
		#PIL.Image.save保存到内存：https://blog.csdn.net/sdlypyzq/article/details/108197715
		frames=[Image.fromarray(frame) if isinstance(frame,np.ndarray) else frame for frame in frames]
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
	@staticmethod
	def Func_ThreadForceStop(th):#线程强制终止
		ctypes.pythonapi.PyThreadState_SetAsyncExc(th.ident, ctypes.py_object(SystemExit))

