
__all__=['XJ_Array2D']

class XJ_Array2D:
	__data=None#早知道那么麻烦，核心就该用np.array了
	def __init__(self):
		self.__data=[]
	def __getitem__(self,pos):
		if(hasattr(pos,'__iter__')):
			rx,ry=pos
		else:
			rx=pos
			ry=slice(None,None,None)
		sliceX,sliceY=True,True
		if(not isinstance(rx,slice)):
			rx=slice(rx,rx+1,1)
			sliceX=False
		if(not isinstance(ry,slice)):
			ry=slice(ry,ry+1,1)
			sliceY=False
		self.__Expand(rx,ry)
		rst=self.__data[rx]
		for x in range(len(rst)):
			rst[x]=rst[x][ry]

		if(len(rst)==1 and not sliceX):
			rst=rst[0]
			if(len(rst)==1 and not sliceY):
				rst=rst[0]
		elif(len(rst[0])==1 and not sliceY):
			for x in range(len(rst)):
				rst[x]=rst[x][0]
		return rst
	def __setitem__(self,pos,val):
		rx,ry=pos
		if(not isinstance(rx,slice)):
			rx=slice(rx,rx+1,1)
		if(not isinstance(ry,slice)):
			ry=slice(ry,ry+1,1)
		self.__Expand(rx,ry)
		self.__data[rx]
		count=len(self.__data[0][ry])
		for data in self.__data[rx]:
			data[ry]=[val]*count
	def __repr__(self):
		rst='\n'.join([str(row) for row in self.__data])
		return f'[{rst}]'
	def data(self):
		return self.__data
	def size(self):
		return (len(self.__data),len(self.__data[0]))
	def __Expand(self,rw,rh):
		data=self.__data
		w,h=rw.stop,rh.stop
		if(w==None):
			w=rw.start
			if(w==None):
				w=1
			w+=1
		if(h==None):
			h=rh.start
			if(h==None):
				h=1
			h+=1
		w,h=w-1,h-1
		for i in range(w-len(data)+1):
			data.append([])
		for i in range(w+1):
			data[i].extend([None for i in range(h-len(data[i])+1)])
