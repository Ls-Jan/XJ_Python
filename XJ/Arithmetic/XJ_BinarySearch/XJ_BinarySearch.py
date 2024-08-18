


__version__='1.0.0'
__author__='Ls_Jan'

__all__=['XJ_BinarySearch']

def XJ_BinarySearch(lst:list,val,inverse:bool=False):
	'''
		二分查找，主用于列表数据插入，同时支持列表倒序。
		网上那代码很多都不去找插入点，就挺搞，基本就完成个“找不到就返回-1”的功能。

		假定lst=[0,2]，
		传入的val值与返回的结果为：(-1,0)、(0,0)、(1,1)、(2,1)、(3,2)
	'''
	L=0
	R=len(lst)-1
	M=-2
	if(inverse):
		if(val<lst[R]):
			M=R+1
		elif(val>=lst[0]):
			M=L
	else:
		if(val>lst[R]):
			M=R+1
		elif(val<=lst[0]):
			M=L
	if(M==-2):
		while(L<=R):
			M=(L+R)>>1
			if(val==lst[M]):
				break
			elif((val<lst[M]) ^ inverse):
				R=M-1
			else:
				L=M+1
		if(inverse):#这是必须的，单独进行修正
			if(val>=lst[M]):
				M-=1
		else:
			if(val<=lst[M]):
				M-=1
		if((val>lst[M]) ^ inverse):#这是必须的，单独进行修正
			M+=1
	return M

