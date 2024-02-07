
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtGui import QPixmap,QGuiApplication,QPainter,QTransform
from PyQt5.QtCore import QRect
from functools import reduce

def GrabScreen(screenID=0):
	'''
		考虑到跨平台问题，没用到与Windows直接相关的东西(像是win32gui啥的)
		
		使用Qt的截屏，返回QPixmap和QRect。后期可以使用QPixmap.copy来截取指定区域
		负值则全截，无效正值则返回空QPixmap和空QRect
	'''
	screens=QGuiApplication.screens()
	if(0<=screenID<len(screens)):
		screen=screens[screenID]
		return screen.grabWindow(0),screen.geometry()
	elif(screenID<0):
		lstRect=[screen.geometry() for screen in screens]
		lstPix=[screen.grabWindow(0) for screen in screens]

		#两矩形区域合并QRect.united：https://doc.qt.io/qt-6/qrect.html#united
		#设置变换QPainter.setTransform：https://doc.qt.io/qt-6/qtransform.html#rendering-graphics
		rect=reduce(lambda rectA,rectB:rectA.united(rectB),lstRect)
		trans=QTransform()
		trans.translate(rect.left(),-rect.top())
		pix=QPixmap(rect.size())
		ptr=QPainter(pix)
		ptr.setTransform(trans)
		for i in range(len(lstRect)):
			ptr.drawPixmap(lstRect[i],lstPix[i])
		ptr.end()
		return pix,rect
	else:
		return QPixmap(),QRect()
