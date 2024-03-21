from ..XJ_GIFMaker import *

from PyQt5.QtWidgets import QFileDialog,QApplication
import cv2

if True:
	app=QApplication([])
	path=QFileDialog.getOpenFileName(None,"载入资源文件","C:/Users/Administrator/Desktop/",filter='*.png;*.jpg;*.mp4;*.gif;*.webp')[0]
	if(path):
		gm=XJ_GIFMaker()
		gm.Opt_Insert(path)
		for frame in gm.frames[::5]:
			im=frame.data()
			im=cv2.cvtColor(im,cv2.COLOR_BGRA2RGBA)
			cv2.imshow('pict',im)
			cv2.waitKey(gm.duration)


