
__version__='1.1.0'
__author__='Ls_Jan'

from .XJ_Test import XJ_Test

import os
import time
import sys

__all__=['XJ_PackageInfo']
class XJ_PackageInfo:
	'''
		获取包信息
	'''
	__name:str#包名
	__mTime:float#修改时间(s)
	__hasTest:bool#有无测试文件
	__path:str#包路径
	def __init__(self,path:str,name:str):
		'''
			path:包所在目录；
			name:包名；
		'''
		root=os.path.join(path,name)
		lst=next(os.walk(root))[2]+['.']
		lst=map(lambda path:os.path.join(root,path),lst)
		lst=map(lambda path:os.path.getmtime(path),lst)
		mTime=max(lst)
		self.__name=name
		self.__path=path
		self.__mTime=mTime
		self.__hasTest=os.path.isfile(os.path.join(root,'Test.py'))
	def Get_Name(self):
		'''
			返回包名称
		'''
		return self.__name
	def Get_MTime(self,format:str='[%Y/%m/%d]%H:%M:%S'):
		'''
			返回包的最近一次修改时间，
			如果format为None则返回浮点数
		'''
		return time.strftime('[%Y/%m/%d]%H:%M:%S',time.localtime(self.__mTime)) if format else self.__mTime
	def Get_Test(self,returnBool:bool=False):
		'''
			包里头需要有一个名为Test.py的测试样例脚本，里头有一个继承了XJ_Test的Test类。
			调用XJ_Test.Opt_Run()运行测试样例。

			returnBool为真时只判断有无测试样例，
			returnBool为假时将获取测试样例(XJ_Test对象，如果没有则返回None)。
		'''
		if(returnBool):
			return self.__hasTest
		test=None
		if(self.__hasTest):
			path=os.path.join(self.__path,self.__name,'Test')
			path=os.path.realpath(path)
			path=path.replace('\\','/')
			path=path.split('/')
			modPath=[]
			while(len(path)>1):
				mod=path.pop()
				if(mod.isidentifier()):
					modPath.append(mod)
			modPath.reverse()

			path=os.path.join(*path)+'/'#得接个斜杠才好使，原因不详
			sys.path.append(path)
			exec(f"from {'.'.join(modPath)} import Test")
			test:XJ_Test=eval('Test()')
			sys.path.pop()
		return test
