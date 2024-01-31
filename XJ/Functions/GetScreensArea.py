
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QRect

def GetScreensArea(*,joint=False):
	'''
		考虑到跨平台问题，没用到与Windows直接相关的东西(像是win32gui啥的)

		获取所有屏幕的位置信息(list-QRect)。
		如果joint为真，则返回合并后的坐标(QRect)
	'''
	screens=QGuiApplication.screens()
	if(joint):
		rect=QRect()
		#两矩形区域合并QRect.united：https://doc.qt.io/qt-6/qrect.html#united
		for s in screens:
			rect=rect.united(s.geometry())
		return rect
	return [screen.geometry() for screen in screens]


