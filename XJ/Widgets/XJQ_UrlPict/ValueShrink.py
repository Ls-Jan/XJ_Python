
__version='1.0.0'
__author__='Ls_Jan'
__all__=['ValueShrink']

class ValueShrink:
	'''
		将一个数通过分段函数进行缩小
	'''
	def __init__(self,start=200,step=50,delta=5):
		'''
			自start起，以step为分段，值的增长以百分比delta逐渐减少
		'''
		self.__start=start
		self.__step=step
		self.__delta=delta
	def Shrink(self,val:int):
		'''
			将一个数缩小并返回
		'''
		start=self.__start
		step=self.__step
		delta=self.__delta

		rate=100
		val=int(val)
		rst=min(val,start)*rate
		val-=start
		while(val>0):
			rate-=delta
			rst+=rate*step
			if(rate<0):
				break
			val-=step
		return rst/100
	@staticmethod
	def GroupShrink(values:tuple,*shrinks,_min:bool=True):
		'''
			将一组数进行等比例缩小，比例选其中的最值(_min为真则取最小，否则取最大)。
			shrinks为ValueShrink对象。
		'''
		rate=[]
		for i in range(min(len(values),len(shrinks))):
			rate.append(shrinks[i].Shrink(values[i])/values[i])
		rate=min(rate) if _min else max(rate)
		return tuple([int(values[i]*rate) for i in range(len(values))])
		

		
