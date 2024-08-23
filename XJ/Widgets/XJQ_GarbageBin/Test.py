
__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from ...ModuleTest import XJQ_Test
from .XJQ_GarbageBin import XJQ_GarbageBin
from ..XJQ_ClipboardDrag import XJQ_ClipboardDrag

from PyQt5.QtWidgets import QWidget,QHBoxLayout
from PyQt5.QtCore import QMimeData
import os

def PrintMimeData(mData:QMimeData):
	os.system('cls')#清屏
	attrLst=[
		('hasText','text'),
		('hasHtml','html'),
		('hasUrls','urls'),
		('hasImage','imageData'),
	]
	for attr in attrLst:
		if(getattr(mData,attr[0])()):
			print(f"【{attr[1]}】")
			print(getattr(mData,attr[1])())
			print('\n\n')

class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		cd=XJQ_ClipboardDrag()
		gb=XJQ_GarbageBin()
		gb.dropped.connect(PrintMimeData)

		wid=QWidget()
		vbox=QHBoxLayout(wid)
		vbox.addWidget(cd)
		vbox.addWidget(gb)
		self.__wid=wid
	def Opt_Run(self):
		print('左边剪切板，右边垃圾桶，试着把数据拖拽进垃圾桶并查看控制台的输出')
		self.__wid.resize(640,480)
		self.__wid.show()
		super().Opt_Run()
		return self.__wid






