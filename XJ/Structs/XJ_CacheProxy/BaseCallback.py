__author__='Ls_Jan'
__version__='1.0.0'
__all__=['BaseCallback']

class BaseCallback:
	'''
		回调类，子类需重写__call__函数，返回布尔值用于判断数据是否有效。
		不使用闭包是为了其他语言着想(虽然也没必要就是了)
	'''
	def __call__(self,data:bytes,valid:bool):
		return valid
