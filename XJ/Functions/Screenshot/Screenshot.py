__version__='1.0.0'
__author__='Ls_Jan'
__all__=['Screenshot']

from PyQt5.QtGui import QPixmap,QGuiApplication,QPainter
from PyQt5.QtCore import QRect,Qt
from typing import Union

def Screenshot(area:Union[QRect,tuple,list]):
	'''
		跨屏截图，返回QPixmap。
		如果需要传入tuple/list作为area，格式应为LTWH，即左上宽高

		考虑到跨平台问题，使用的是Qt截屏功能，没用到与Windows直接相关的东西(像是win32gui啥的)，
		因此必须创建QApplication对象后才能调用该函数。
	'''
	if(isinstance(area,tuple) or isinstance(area,list)):
		area=QRect(*area[:4])
	screens=QGuiApplication.screens()
	rst=QPixmap(area.size())
	rst.fill(Qt.GlobalColor.transparent)
	ptr=QPainter(rst)
	for screen in screens:
		areaS=screen.geometry()
		areaT=areaS.intersected(area)
		if(not areaT.isEmpty()):#数据有效
			areaP=QRect(areaT)
			areaP.moveTopLeft(areaP.topLeft()-areaS.topLeft())
			pix=screen.grabWindow(0,areaP.left(),areaP.top(),areaP.right(),areaP.bottom())
			ptr.drawPixmap(areaT.topLeft()-area.topLeft(),pix)
	ptr.end()
	return rst


