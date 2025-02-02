__author__='Ls_Jan'
__version__='1.0.0'
__all__=['_Urls']

class _Urls:
	'''
		记录请求的url(带payload数据)
	'''
	requesting:set
	success:set
	fail:set
	def __init__(self):
		self.requesting=set()
		self.success=set()
		self.fail=set()


