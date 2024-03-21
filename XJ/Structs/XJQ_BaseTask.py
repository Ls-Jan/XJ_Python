
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtCore import QRunnable

__all__=['XJQ_BaseTask']
class XJQ_BaseTask(QRunnable):
	'''
		继承了QRunnable的任务抽象类，传入id、任务完成时的回调函数callback，
		回调函数接受两个参数(id,result)，其中的result是doTask执行后的返回结果。

		该类不能实例化，必须继承并重写doTask()以实现相关业务逻辑。
		(原本是想将本类使用ABCMeta强制抽象化，奈何总是报错，懒得深究
	'''
	def __init__(self,id,callback):
		super().__init__()
		self.__callback=callback
		self.__id=id
	def doTask(self)->None:
		raise Exception('从XJQ_BaseTask中派生的任务类必须重写doTask')
	def run(self)->None:
		result=self.doTask()
		self.__callback(self.__id,result)


