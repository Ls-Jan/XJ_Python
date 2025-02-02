

'''
	给定随机数据，
	限制宽度后会将数据进行分组，

	例如给定数据[53,75,64,26,41]，宽度100，
	分组后得到[53,41]、[64,26],[75]，
	分组结果可不唯一
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



#函数First和Second为核心
def First(remainingIndices,source,width):
	'''
		在给定的源数据source和限制宽度width中，
		根据剩余索引remainingIndices，
		首次获取索引列表row(同时会修改remainingIndices的内容)
	'''
	rest=width
	row=[]
	for index in remainingIndices:
		if(rest>source[index]):
			rest-=source[index]
			row.append(index)
	for index in row:
		remainingIndices.remove(index)
	return row
def Second(row,remainingIndices,source,width):
	'''
		在给定的源数据source和限制宽度width中，
		根据剩余索引remainingIndices，
		对索引列表row进行进一步的细化，使结果逐渐逼近限制宽度width。

		每次成功时row长度都会+1，同时会修改remainingIndices的内容，并且返回真。
		连续调用Second函数直到row无法细化为止。
	'''
	threshold=width-sum([source[index] for index in row])
	records=[]
	for i in range(len(row)-1,0,-1):
		removeIndex=row[i]
		record=[removeIndex]#4个元素，移除index、两个加入index，新差值
		for startIndex in remainingIndices:
			record=[removeIndex]
			rest=threshold+source[removeIndex]
			count=0
			if(startIndex<=removeIndex):
				continue
			flag=False
			for index in remainingIndices[remainingIndices.index(startIndex):]:
				if(index<startIndex):
					continue
				if(rest>=source[index]):
					rest-=source[index]
					record.append(index)
					count+=1
					if(count==2):
						if(rest<threshold):
							records.append(record)
							record.append(rest)
							flag=True
						break
			if(flag):
				break
	if(not records):
		return False
	records.sort(key=lambda record:record[-1])
	record=records[0]#只取差值最小的
	row.remove(record[0])
	row.append(record[1])
	row.append(record[2])
	remainingIndices.append(record[0])
	remainingIndices.remove(record[1])
	remainingIndices.remove(record[2])
	remainingIndices.sort()
	return True


if __name__=='__main__':
	random.seed(5)#设置随机数，方便debug重现

	width=500#宽度
	source=sorted(CreateRandomLst(20),reverse=True)#源数据，从大到小进行排列
	remainingIndices=list(range(len(source)))#剩余索引(总是从小到大排列)

	record=[]
	while(remainingIndices):
		row=First(remainingIndices,source,width)
		while(Second(row,remainingIndices,source,width)):
			pass
		record.append(row)

	print("源数据：",source)
	print("限制宽度：",width)
	print()
	print("分组结果如下(第一个数据是列表和)：")
	for row in record:
		lst=list(map(lambda index:source[index],row))
		print(sum(lst),lst)












