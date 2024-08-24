__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_ClipboardDrag']

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap,QColor,QMouseEvent,QPainter,QTextDocument,QDrag,QFont
from PyQt5.QtCore import QSize,Qt,QMimeData,QRect,QRectF
from ...Structs.XJ_MouseStatus import XJ_MouseStatus
from ...Functions.GetRealPath import GetRealPath
from ..XJQ_AutoSizeLabel import XJQ_AutoSizeLabel
from typing import Union

class XJQ_ClipboardDrag(XJQ_AutoSizeLabel):
	'''
		一个剪切板控件，拖拽本控件相当于拖拽剪切板的数据。

		补充：
			1.无法获取QQ截图的图片信息，因为QQ截图的图片数据并没有直接存放在剪切板中，目前暂时不知道获取手段，猜测可能使用了winAPI；
			2.有时会出现不知名的系统原因，QMimeData受到损坏，无法放置图片数据，而这不仅导致剪切板无法放置图片，拖拽事件也无法携带图片数据；
			3.尽管剪切板的QMimeData可能是坏的，依旧可以通过QClipboard.image/pixmap的方式获取剪切板的图片数据，
				虽然如此也不能解决什么问题，因为拖拽的QMimeData一旦损坏那么该剪切板控件拖出来的图片数据也不能信任，只能说，太棘手了；
	'''
	def __init__(self,icon:Union[QPixmap,str]=None,dragPreviewPixmap:QPixmap=None,size:QSize=QSize(128,128),minSize:QSize=QSize(64,64)):
		'''
			接受一个剪切板图标，可传入文件路径或是QPixmap对象，如果传入空则使用默认图标。
			图标可以通过setPixmap进行替换。
			dragPreviewPixmap为拖拽时的默认预览图，可以通过Set_DragPreviewDefaultPixmap进行设置。
			size为控件图标大小，minSize为控件最小大小。
		'''
		super().__init__()
		self.__ms=XJ_MouseStatus()
		self.setAcceptDrops(True)
		if(icon==None):
			icon=GetRealPath('./图标-剪贴板.png')
		if(isinstance(icon,str)):
			icon=QPixmap(icon)
		self.setPixmap(icon.scaled(size))
		self.setMinimumSize(minSize)
		self.__previewSize=QSize(400,160)
		self.__previewPix=None
		self.Set_DragPreviewDefaultPixmap(dragPreviewPixmap)

		#特殊说明：
		#此处专门用来消耗掉QPainter初次绘制文本时造成的卡顿问题
		pix=QPixmap(1,1)
		ptr=QPainter(pix)
		ptr.drawText(0,0,"ABC")
		ptr.end()
	def Set_DragPreviewDefaultPixmap(self,pix:QPixmap):
		'''
			设置拖拽时预览图的图片显示，传入空则使用纯色淡蓝
		'''
		if(not pix):
			pix=QPixmap(QSize(160,160))
			pix.fill(QColor(200,224,248,176))
		self.__previewPix=pix
	def Set_DragPreviewSize(self,size):
		'''
			设置拖拽时的预览图大小
		'''
		self.__previewSize=size
	def mousePressEvent(self,event):
		self.__ms.Opt_Update(event)
	def mouseMoveEvent(self,event):
		ms=self.__ms
		ms.Opt_Update(event)
		btn,status=ms.Get_PressButtonStatus()
		if(btn==Qt.MouseButton.LeftButton and status==QMouseEvent.MouseButtonPress and ms.Get_HasMoved(True)):#左键拖拽
			cb=QApplication.clipboard()
			mDataSrc=cb.mimeData()
			mData=QMimeData()
			for fmt in mDataSrc.formats():#无脑全复制
				mData.setData(fmt,mDataSrc.data(fmt))
			if(mData.hasImage()):#特别处理，只不过就算这么做，拖拽事件的QMimeData中的图片数据也是无效的
				mData.setImageData(cb.image())
			dg=QDrag(self)
			dg.setPixmap(self.Get_Preview(mData,self.__previewPix,self.__previewSize))
			dg.setMimeData(mData)
			dg.exec(Qt.DropAction.CopyAction)#不使用MoveAction，它并不实用。绝大多数场合下的拖拽都是复制的
	@staticmethod
	def Get_Preview(mData:QMimeData,empytFilePixmap:QPixmap,size:QSize=QSize(400,160)):
		'''
			获取QMimeData数据内容的简单渲染(返回QPixmap)；
			emptyFilePixmap决定默认预览图；
			size决定预览图宽高；
		'''
		im=mData.imageData()
		urls=mData.urls()
		text=mData.text()
		html=mData.html()		
		W,H=size.width(),size.height()
		pix=QPixmap(W,H)
		pix.fill(Qt.transparent)
		ptr=QPainter(pix)
		doc=QTextDocument()
		if(im or urls):
			if(not im):
				im=empytFilePixmap.toImage()
			imW=im.width()
			imH=im.height()
			rate=min(W/imW,H/imH)
			imW=imW*rate
			imH=imH*rate
			ptr.drawImage(QRect(0,0,imW,imH),im)
			cnt=len(urls)
			if(cnt>1):
				ptr.setFont(QFont("",20))
				doc.setPlainText(str(cnt))
				ptr.drawText(int(imW-doc.size().width())>>1,int(imH+doc.size().height())>>1,str(cnt))#在大概中心的位置绘制数字
		elif(text or html):
			ptr.setFont(QFont("",14))
			if(text):
				doc.setPlainText(text)
			else:
				doc.setHtml(html)
			doc.drawContents(ptr,QRectF(0,0,W,H))
		ptr.end()
		return pix

