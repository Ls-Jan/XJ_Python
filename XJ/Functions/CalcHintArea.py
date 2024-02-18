from typing import Union
from PyQt5.QtCore import QSize,QRect,QPoint

__all__=['CalcHintArea']
def CalcHintArea(
				target:Union[QRect,QPoint],
				hSize:QSize,
				pSize:QSize,
				margin:int=0,
				excludeMargin:bool=False,
				priority='RBLT'):
	'''
		根据指定参数计算弹窗的相对位置，
		将依次返回：实际目标坐标(QPoint)、弹窗所在方位('LTRB'之一)、弹窗所在区域(QRect)。
		如果target脱离pSize范围则会返回None

		target：目标坐标，弹窗将在target周围位置显示(如果可能的话)，可以是QRect
		hSize：弹窗大小
		pSize：区域大小，可以理解成弹窗将在QRect(QPoint(0,0),pSize)范围内显示
		margin：弹窗与target的间距
		excludeMargin：当该值为真时返回的弹窗区域将不包含margin的部分
		priority：弹窗位置优先级
	'''
	if(isinstance(target,QPoint)):
		target=QRect(target,target)
	hW,hH=hSize.width(),hSize.height()
	pW,pH=pSize.width(),pSize.height()
	lst=[]
	if(QRect(QPoint(0,0),pSize).intersects(target)):
		for p in priority:
			L,T,R,B=target.left(),target.top(),target.right(),target.bottom()
			if(p=='L'):
				area=QRect(QPoint(0,0),QPoint(min(L,pW),pH))
				line=QRect(target.topLeft(),target.bottomLeft())
			elif(p=='R'):
				area=QRect(QPoint(max(0,R),0),QPoint(pW,pH))
				line=QRect(target.topRight(),target.bottomRight())
			elif(p=='T'):
				area=QRect(QPoint(0,0),QPoint(pW,max(0,T)))
				line=QRect(target.topLeft(),target.topRight())
			elif(p=='B'):
				area=QRect(QPoint(0,min(B,pH)),QPoint(pW,pH))
				line=QRect(target.bottomLeft(),target.bottomRight())
			else:
				continue
			newline=area.intersected(line)
			if(newline and area):
				W,H=hW,hH
				if(p in 'LR'):
					W+=margin
				else:
					H+=margin
				aW=area.width()
				aH=area.height()
				lst.append((
					newline.center(),
					p,
					area,
					min(aW,W)*min(aH,H)))
				if(aW>W and aH>H):#空间充裕
					if(not area.contains(line)):#边界被截过，作为次要判断
						continue
					else:#理想情况
						lst=lst[-1:]
						break
		if(lst):
			lst.sort(key=lambda item:(-item[3],priority.index(item[1])))
			target,p,area=lst[0][:3]
			x,y=target.x(),target.y()
			W,H=hW,hH
			if(p in 'LR'):
				W+=margin
				if(p =='L'):
					area.setLeft(area.right()-W+1)
					if(excludeMargin):
						area.setRight(area.right()-margin)
				else:
					area.setRight(area.left()+W-1)
					if(excludeMargin):
						area.setLeft(area.left()+margin)
				aT=area.top()+H/2
				aB=area.bottom()-H/2
				if(aT>y):
					aB=aT
				elif(aB<y):
					aT=aB
				else:
					aT=y
					aB=y
				aT-=H/2-1
				aB+=H/2
				area.setTop(aT)
				area.setBottom(aB)
			else:
				H+=margin
				if(p =='T'):
					area.setTop(area.bottom()-H+1)
					if(excludeMargin):
						area.setBottom(area.bottom()-margin)
				else:
					area.setBottom(area.top()+H-1)
					if(excludeMargin):
						area.setTop(area.top()-margin)
				aL=area.left()+W/2
				aR=area.right()-W/2
				if(aL>x):
					aR=aL
				elif(aR<x):
					aL=aR
				else:
					aL=x
					aR=x
				aL-=W/2-1
				aR+=W/2
				area.setLeft(aL)
				area.setRight(aR)
			return target,p,area
	return None
