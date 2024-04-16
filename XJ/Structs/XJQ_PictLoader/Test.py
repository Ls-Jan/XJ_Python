
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
# from ..XJ_Frame import XJ_Frame
from ..XJ_GIFMaker import XJ_GIFMaker
from ..XJQ_PictLoader import XJQ_PictLoader
from ...Functions.GetRealPath import GetRealPath
# from ...Functions.CV2ToQPixmap import CV2ToQPixmap

from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QListView
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QIcon
from PyQt5.QtCore import QSize

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		wid=QWidget()
		vbox=QVBoxLayout(wid)
		btnL=QPushButton('Load')
		btnC=QPushButton('Clear')
		lv=QListView()
		vbox.addWidget(btnL)
		vbox.addWidget(btnC)
		vbox.addWidget(lv)
		lvModel=QStandardItemModel()
		lv.setModel(lvModel)
		lv.setIconSize(QSize(64,64))

		self.__wid=wid
		self.__btnL=btnL
		self.__btnC=btnC
		self.__lvModel=lvModel
	def Opt_Run(self):
		self.__wid.resize(800,400)
		self.__wid.show()
		print("需要选择一个动图以查看效果")
		file=self.Get_File(GetRealPath('../../Icons/Loading/加载动画-7.gif'),'请选择动图文件')
		if(file):
			print('图片数据将逐个加载，不会有明显卡顿')
			gm=XJ_GIFMaker()
			gm.Opt_Insert(file)
			for i in range(len(gm.frames)):
				self.__lvModel.appendRow(QStandardItem(str(i)))

			pl=XJQ_PictLoader()
			pl.loaded.connect(lambda id,pix:self.__lvModel.item(id).setIcon(QIcon(pix)))
			self.__btnL.clicked.connect(lambda:pl.Opt_Append(*[(i,gm.frames[i]) for i in range(len(gm.frames))]))
			self.__btnC.clicked.connect(lambda:pl.Opt_Clear() or [self.__lvModel.item(i).setIcon(QIcon()) for i in range(len(gm.frames))])
		else:
			print("请重新运行测试样例")
		super().Opt_Run()
		return self.__wid

