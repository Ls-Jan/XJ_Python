__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_ClipboardDrag']
#TODO：2024/8/18
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from XJ.Structs.XJ_MouseStatus import XJ_MouseStatus
from XJ.Functions.GetRealPath import GetRealPath


class XJQ_ClipboardDrag(QLabel):
	'''
		一个剪切板控件，
		拖拽本控件相当于拖拽剪切板的数据。
		图标自己设置，这里不负责。
	'''
	def __init__(self,emptyImage):
		super().__init__()
		self.__ms=XJ_MouseStatus()
		self.setAcceptDrops(True)
	# def Set_Pixmap(self,emptyFile:QPixmap,):

	def mousePressEvent(self,event):
		self.__ms.Opt_Update(event)
	def mouseMoveEvent(self,event):
		ms=self.__ms
		ms.Opt_Update(event)
		btn,status=ms.Get_PressButtonStatus()
		if(btn==Qt.MouseButton.LeftButton and status==QMouseEvent.MouseButtonPress and ms.Get_HasMoved(True)):#左键拖拽
			mDataSrc=QApplication.clipboard().mimeData()
			mData=QMimeData()
			for fmt in mDataSrc.formats():#无脑全复制
				mData.setData(fmt,mDataSrc.data(fmt))
			dg=QDrag(self)
			self.Get_Preview(mData,)
			dg.setMimeData(mData)
			dg.exec(Qt.DropAction.MoveAction)
	def dragEnterEvent(self,event:QDragEnterEvent):
		return
	# def dragEnterEvent(self,event):
		event.setDropAction(Qt.DropAction.IgnoreAction)
		mData=QMimeData()

		# event.ignore()
		# print(event)
		# event.acceptProposedAction()
		event.accept()
		mDataSrc=event.mimeData()
		for fmt in mDataSrc.formats():
			print(fmt)
			print(mDataSrc.data(fmt))
			print()
		return
		mDataSrc=event.mimeData()
		mData=QMimeData()
		for fmt in mDataSrc.formats():#无脑全复制
			mData.setData(fmt,mDataSrc.data(fmt))
		QApplication.clipboard().setMimeData(mData)
		for fmt in mDataSrc.formats():
			print(fmt)
			print(mDataSrc.data(fmt))
			print()
		# event.setDropAction(Qt.MoveAction)
		event.acceptProposedAction()
	def dragMoveEvent(self,event):
		return
		print(event)
	@staticmethod
	def Get_Preview(mData:QMimeData,empytFileImage:QImage,WH:tuple=(400,160)):
		'''
			获取QMimeData数据内容的简单渲染(返回QPixmap)；
			emptyFileImage决定默认预览图；
			WH决定宽高；
		'''
		im=mData.imageData()
		urls=mData.urls()
		text=mData.text()
		html=mData.html()

		W,H=WH
		pix=QPixmap(W,H)
		pix.fill(Qt.transparent)
		ptr=QPainter(pix)
		doc=QTextDocument()
		if(im or urls):
			if(not im):
				im=empytFileImage
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


if True:
	app=QApplication([])
	gb=XJQ_ClipboardDrag()

	mData=QApplication.clipboard().mimeData()
	gb=QLabel()
	pix=XJQ_ClipboardDrag.Get_Preview(mData,QImage(GetRealPath('./图标-未知文件.ico')))
	gb.setPixmap(pix)

	gb.show()
	gb.resize(640,480)
	app.exec()


