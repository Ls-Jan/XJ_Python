__author__='Ls_Jan'
__version__='1.0.0'
__all__=['BaseCallback']

class BaseCallback:
	'''
		回调类，子类需重写__call__函数
	'''
	def __call__(self,url:str,data:bytes):
		pass
