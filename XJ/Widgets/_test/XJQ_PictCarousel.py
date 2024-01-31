from ..XJQ_PictCarousel import *
from ...Functions import GetRealPath

if True:
	app = QApplication([])

	file='../icons/加载动画-1.gif'
	# file='图片.gif'
	# file='Clock_JE3_BE3.webp'
	file=GetRealPath(file)
	im = Image.open(file)
	im.load()#调用该函数后info中的信息才会有效(这是试出来的)

	lst=[]
	size=im.size
	for i in range(im.n_frames):
		im.seek(i)
		if(im.mode!="RGBA"):#Debug半小时，真够恶心，0帧往往是P模式(调色板)，获取到的数据是缺失的
			b=im.convert("RGBA").tobytes()
		else:
			b=im.tobytes()
		pix=QPixmap(QImage(b, *size, size[0]*4,QImage.Format_RGBA8888))
		lst.append(pix)

	t=XJQ_PictCarousel()
	# t.Set_Interval(100)
	t.Set_Interval(0)
	t.Set_Duration(100)
	# t.Set_Duration(im.info.get('duration',50))
	t.Set_Frames(lst)
	t.show()
	t.resize(1200,700)
	# t.setStyleSheet('background:#222222;')

	app.exec_()

