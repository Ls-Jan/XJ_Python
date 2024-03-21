
__version__='1.1.1'
__author__='Ls_Jan'

from typing import Union
from PyQt5.QtCore import QSize,QRect,QPoint

__all__=['CalcPopupArea']

def GetTupleFromRect(rect):
	return rect.left(),rect.top(),rect.right(),rect.bottom()

def GetNearestPoint(pos,rect,corner):
	'''
		获取矩形中离pos最近的点(QPoint)，如果corner为真那么可选值约束为矩形的四点之一
	'''
	rect=rect.normalized()
	L,T,R,B=GetTupleFromRect(rect)
	x,y=pos.x(),pos.y()
	if(corner):
		x=L if abs(x-L)<abs(x-R) else R
		y=T if abs(y-T)<abs(y-B) else B
	else:
		lst=[]
		for item in [(x,L,R),(y,T,B)]:
			val,a,b=item
			val=a if val<a else b if val>b else val
			lst.append(val)
		x,y=lst
	return QPoint(x,y)
def GetLimitRect(rect,area):
	'''
		获取经area约束后的rect(大小不变，仅调整位移)
	'''
	lst=[]
	for item in [
			(rect.left(),rect.right(),area.left(),area.right()),
			(rect.top(),rect.bottom(),area.top(),area.bottom()),]:
		rL,rR,aL,aR=item
		if(rR-rL>aR-aL):
			rL,rR=aL,aR
		else:
			d1=aL-rL
			d2=aR-rR
			if(d1>0):
				rL=aL
				rR+=d1
			if(d2<0):
				rL+=d2
				rR=aR
		lst.append((rL,rR))
	LR,TB=lst
	return QRect(QPoint(LR[0],TB[0]),QPoint(LR[1],TB[1]))
	

def CalcPopupArea(
				target:Union[QRect,QPoint],
				hSize:QSize,
				area:Union[QRect,QSize],
				margin:int=0,
				excludeMargin:bool=False,
				corner:bool=False,
				priority='RBLT'):
	'''
		根据指定参数计算弹窗的相对位置，
		将依次返回：实际目标坐标(QPoint)、弹窗所在方位('LTRB'之一)、弹窗所在区域(QRect)。
		如果target脱离area范围则会返回None

		target：目标坐标，弹窗将在target周围位置显示(如果可能的话)，可以是QRect；
		hSize：弹窗大小；
		area：区域范围，弹窗将尽可能在该区域内显示，如果area是QSize那么将视作QRect(QPoint(0,0),area)；
		margin：弹窗与target的间距；
		excludeMargin：当该值为真时返回的弹窗区域将不包含margin的部分；
		priority：弹窗位置优先级；
		
		【新增】corner：该值为真时会将弹窗的边角尽可能移动到target附近，使其效果更贴近“右键菜单”
	'''

	if(isinstance(target,QPoint)):
		target=QRect(target,target)
	hW,hH=hSize.width(),hSize.height()
	if(isinstance(area,QSize)):
		area=QRect(QPoint(0,0),area)
	lst=[]
	if(area.intersects(target)):
		aL,aT,aR,aB=GetTupleFromRect(area)
		for p in priority:
			L,T,R,B=GetTupleFromRect(target)
			if(p=='L'):
				area=QRect(QPoint(aL,aT),QPoint(min(L,aR),aB))
				line=QRect(target.topLeft(),target.bottomLeft())
			elif(p=='R'):
				area=QRect(QPoint(max(aL,R),aT),QPoint(aR,aB))
				line=QRect(target.topRight(),target.bottomRight())
			elif(p=='T'):
				area=QRect(QPoint(aL,aT),QPoint(aR,max(aT,T)))
				line=QRect(target.topLeft(),target.topRight())
			elif(p=='B'):
				area=QRect(QPoint(aL,min(B,aB)),QPoint(aR,aB))
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
			rect=QRect(area)
			x,y=target.x(),target.y()
			W,H=hW,hH
			if(p in 'LR'):
				W+=margin
				if(p =='L'):
					rect.setLeft(rect.right()-W+1)
					if(excludeMargin):
						rect.setRight(rect.right()-margin)
				else:
					rect.setRight(rect.left()+W-1)
					if(excludeMargin):
						rect.setLeft(rect.left()+margin)
				rT=rect.top()+H/2
				rB=rect.bottom()-H/2
				if(rT>y):
					rB=rT
				elif(rB<y):
					rT=rB
				else:
					rT=y
					rB=y
				rT-=H/2-1
				rB+=H/2
				rect.setTop(rT)
				rect.setBottom(rB)
			else:
				H+=margin
				if(p =='T'):
					rect.setTop(rect.bottom()-H+1)
					if(excludeMargin):
						rect.setBottom(rect.bottom()-margin)
				else:
					rect.setBottom(rect.top()+H-1)
					if(excludeMargin):
						rect.setTop(rect.top()+margin)
				rL=rect.left()+W/2
				rR=rect.right()-W/2
				if(rL>x):
					rR=rL
				elif(rR<x):
					rL=rR
				else:
					rL=x
					rR=x
				rL-=W/2-1
				rR+=W/2
				rect.setLeft(rL)
				rect.setRight(rR)
			if(corner):
				offset=GetNearestPoint(target,rect,True)-target
				rect.moveTo(rect.topLeft()+offset)
				rect=GetLimitRect(rect,area)
			return target,p,rect
	return None



