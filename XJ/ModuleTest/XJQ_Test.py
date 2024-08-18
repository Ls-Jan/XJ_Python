
__version__='1.0.0'
__author__='Ls_Jan'

from .XJ_Test import XJ_Test
from PyQt5.QtWidgets import QApplication,QFileDialog

__all__=['XJQ_Test']

class XJQ_Test(XJ_Test):
	'''
		继承XJ_Test的泛型，特用于Widgets模块的控件测试。

		Opt_Run需要重写，并主动调用控件的show函数
	'''
	def __init__(self):
		super().__init__()
		app=QApplication.instance()
		if(app==None):
			app=QApplication([])
		self.__app=app
	def Opt_Run(self):
		'''
			可以根据实际需要，返回主控件对象
		'''
		if(self.__app):
			self.__app.exec()
	@staticmethod
	def Get_File(path:str,hint:str='载入资源文件',filter='*.png;*.jpg;*.mp4;*.gif;*.webp'):
		'''
			快速打开一个文件，不再需要在测试模块中额外添加测试文件了
		'''
		path=QFileDialog.getOpenFileName(None,hint,path,filter=filter)[0]
		return path
