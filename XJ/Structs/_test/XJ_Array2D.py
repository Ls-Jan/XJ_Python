
from ..XJ_Array2D import *

if True:
	b=XJ_Array2D()
	b[1,3]=6
	b[1,4]=8
	b[1,5]=10
	print(b)
	# print(b[1:4,5])
	# print(b[1:4,5:6])
	print(b[1:2,4:6])
	print(b[1,4:6])
	print()
	print(b.size())

	# for i in range(b.size()[0]):
		# print(b[i][3:5+1])



