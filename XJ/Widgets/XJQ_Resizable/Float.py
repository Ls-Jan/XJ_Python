
class Float:
	'''
		因为float为只读/不可变类型。
		但又找不到相应的“可变类型”，就只能自己写一个出来顶着用。
	'''
	def __init__(self,val:float):
		self.val=val


