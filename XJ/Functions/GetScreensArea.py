
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtGui import QGuiApplication,QCursor
from PyQt5.QtCore import QRect

__all__=['GetScreensArea']
def GetScreensArea(*,joint:bool=False,includeCursor=False):
	'''
		获取所有屏幕的位置信息(list-QRect)。
		如果joint为真，则直接返回合并后的坐标(QRect)
		如果includeCursor为真那么将返回鼠标所在屏幕的坐标(QRect)

		考虑到跨平台问题，没用到与Windows直接相关的东西(像是win32gui啥的)
	'''
	screens=QGuiApplication.screens()
	if(joint):
		rect=QRect()
		#两矩形区域合并QRect.united：https://doc.qt.io/qt-6/qrect.html#united
		for s in screens:
			rect=rect.united(s.geometry())
		return rect
	screens=[screen.geometry() for screen in screens]
	if(includeCursor):
		pos=QCursor().pos()#获取鼠标位置：https://blog.csdn.net/weixin_43862688/article/details/108180908
		for rect in screens:
			if(rect.contains(pos)):
				return rect
	return screens


