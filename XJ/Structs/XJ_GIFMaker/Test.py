
__version__='1.1.0'
__author__='Ls_Jan'

from ..XJ_GIFMaker import XJ_GIFMaker
from ...ModuleTest import XJQ_Test

import cv2

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self) -> None:
		super().__init__()
	def Opt_Run(self):
		print('读取GIF并使用cv2.imshow逐帧显示')
		path=self.Get_File("C:/Users/Administrator/Desktop/","载入资源文件",'*.png;*.jpg;*.mp4;*.gif;*.webp')
		if(path):
			gm=XJ_GIFMaker()
			gm.Opt_Insert(path)
			for frame in gm.frames[::5]:
				im=frame.data()
				im=cv2.cvtColor(im,cv2.COLOR_BGRA2RGBA)
				cv2.imshow('pict',im)
				cv2.waitKey(gm.duration)
		return
		# return super().Opt_Run()#不需要，因为没使用窗口
