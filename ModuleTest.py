
import os
import time

class XJ_ModTest:
	__parts=[
		'Widgets',
		'Functions',
		'Scripts',
		'Arithmetic',]
	def __init__(self):
		self.__mods={}
	def Opt_GetParts(self):
		return self.__parts
	def Opt_LoadMods(self,part):
		if(part not in self.__parts):
			raise Exception(f'模块{part}不存在')
		mods=[]
		for file in next(os.walk(self.GetPath(part)))[2]:
			if('XJ' in file):
				mod=file[:-3]
				pmod=self.GetPath(part,mod)
				ptmod=self.GetPath(part,mod,test=False)
				mTime=[os.path.getmtime(pmod)]
				if(os.path.exists(ptmod)):
					mTime.append(os.path.getmtime(ptmod))
				mTime=max(mTime)
				mods.append({
					'mod':mod,
					'mTime':mTime,
					'pTest':ptmod,
					'pmTest':self.GetPath(part,mod,seq='.',suffix='')})
		mods.sort(key=lambda item:-item['mTime'])#升序排序
		for item in mods:
			mTime=item['mTime']
			item['mTime']=time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(mTime))
		self.__mods=mods
		return mods
	def Opt_TestMod(self,index=0):
		mod=self.__mods[0]
		print(mod['pmTest'])
		print(mod['mTime'])
		exec(f'import {mod["pmTest"]}')
	@staticmethod
	def GetPath(part,mod='',seq='/',suffix='.py',test=True):
		lst=['XJ',part]
		if(test):
			lst.append('_test')
		if(mod):
			lst.append(f'{mod}{suffix}')
		return seq.join(lst)

if __name__=='__main__':
	mt=XJ_ModTest()
	mt.Opt_LoadMods('Widgets')
	mt.Opt_TestMod()


