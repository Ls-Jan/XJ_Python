

'''
	给定随机数据，将其分成长度尽可能均匀的组，顺序不可打乱

	例如给定数据[53,75,64,26,41]，分成2组，
	分组后得到[53,75]、[64,26,41]
'''


import random


def CreateRandomLst(count):
	'''
		指定个数，创建随机列表
	'''
	longCount=int(count*random.randint(10,25)/100)#超长tag个数
	shortCount=int(count*random.randint(10,20)/100)#超短tag个数
	normalCount=count-longCount-shortCount#普通tag个数
	shortLen=(20,50)
	normalLen=(50,100)
	longLen=(100,150)
	rst=[random.randint(*shortLen) for i in range(shortCount)]+\
		[random.randint(*normalLen) for i in range(normalCount)]+\
		[random.randint(*longLen) for i in range(longCount)]
	random.shuffle(rst)
	return rst


def First(lst:list,rowCount:int,width:int=0):
	'''
		将数据尽可能的均匀分组，
		如果指定推荐宽度width则优先以width为参考值，即如果行宽width大到一定程度时不一定会将行填满(有可能会有几条空行)
	'''
	total=sum(lst)
	average=int(total/rowCount)
	width=max(average,width)
	tmp=0
	row=[]
	groups=[row]
	for data in lst:
		if(tmp+data>width and len(groups)<rowCount):#跨越临值，进行简单的数值比较。如果当前行数已经达到最大，就无法继续开新行，只能将数据加入到末行中
			if(width-tmp<(tmp+data)-width):#说明前者差值更小，即当前数据放在当后一行是较优解(不好说这就是最优解)
				row=[data]
				tmp=data
			else:
				row.append(data)
				row=[]
				tmp=0
			groups.append(row)
		else:
			row.append(data)
			tmp+=data
	for i in range(rowCount-len(groups)):#填补空行
		groups.append([])
	return groups


#该函数没做，等真正需要时再考虑是否完成
#甚至可以考虑直接重新完成First函数
def Second(groups,prev:bool=True,empty:bool=False):
	'''
		根据需求，对初步分组的结果进行进一步的优化，
		- prev为真时会将数据上移，表现结果为数据末行较短，反之将数据下移(表现为首行较短)，
			通常采用prev为真的方案，在视觉上会让人有一种“留有余地”的效果。
		- empty为真则允许出现空行。
	'''
	sums=[sum(row) for row in groups]


import time
if __name__=='__main__':
	seeds=[#测试时如果有特殊种子可以单独进行记录到此处
		1725102968,
		1725104984,
		1725105137,
		1725105277,
		int(time.time()),
	]
	for seed in seeds[:]:
		random.seed(seed)#设置随机数，方便debug重现

		rowCount=3#行数
		source=CreateRandomLst(20)#源数据
		# rst=First(source,rowCount,800)#分组结果(有推荐宽度800，会优先将宽度填满，换句话说就是数据不足时会出现空行)
		rst=First(source,rowCount)#分组结果(无推荐宽度，所有行均会有数据)

		print(f'当前随机数种子：{seed}')
		print('源数据：',int(sum(source)/rowCount),source)
		for row in rst:
			print(sum(row),row)
		print()











