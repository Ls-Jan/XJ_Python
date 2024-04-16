__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .CV2PictExpand import CV2PictExpand
from ..GetRealPath import GetRealPath
from ..CV2LoadPict import CV2LoadPict
import cv2
from matplotlib import pyplot



__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
	def Opt_Run(self):
		print('选择一张图片，之后会将其填充为正方形，为了直观，填充的像素颜色设置为红色')
		file=self.Get_File(GetRealPath('../../Icons/云下载.png'),'选择图片','*.png;*.jpg')
		if(file):
			im=CV2LoadPict(file)
			imNew=CV2PictExpand(im,(255,0,0))
			lst=[('imageOrigin',im),('imageExpand',imNew)]
			for i in range(len(lst)):
				item=lst[i]
				i+=1
				pyplot.subplot(1,2,i)
				pyplot.imshow(item[1])
				pyplot.title(item[0],fontsize=8)
			pyplot.show()
		# return super().Opt_Run()

