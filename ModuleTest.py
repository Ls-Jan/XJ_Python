


# from XJ.Widgets._test.XJQ_PlayBar import *
# from XJ.Widgets._test.XJQ_NumInput import *
# from XJ.Widgets._test.XJQ_PictListView import *
# from XJ.Widgets._test.XJQ_Clock import *
# from XJ.Widgets._test.XJQ_FolderBox import *
# from XJ.Widgets._test.XJQ_ListWidgetItem import *
# from XJ.Functions._test.CV2PictExpand import *
# from XJ.Structs._test.XJ_SQLite import *

# exit()


import os
import time

class XJ_ModTest:
	def __init__(self):
		self.__mods={}
		self.__parts=tuple(filter(lambda name:name[0].isupper(),next(os.walk('XJ'))[1]))
	def Opt_GetParts(self):
		return self.__parts
	def Opt_LoadMods(self,part):
		if(part not in self.__parts):
			raise Exception(f'模块{part}不存在')
		mods=[]
		exclude={'__init__.py'}
		for file in next(os.walk(self.GetPath(part)))[2]:
			if(file not in exclude):
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
			item['mTime']=time.strftime('[%Y/%m/%d]%H:%M:%S',time.localtime(mTime))
		self.__mods=mods
		return mods
	def Opt_TestMod(self,index=0):
		if(0<=index<len(self.__mods)):
			mod=self.__mods[index]
			print(mod['pmTest'])
			# print(mod['mTime'])
			pmTest=mod["pmTest"]
			os.system(f'py -c "import {pmTest}"')
	@staticmethod
	def GetPath(part,mod='',seq='/',suffix='.py',test=True):
		lst=['XJ',part]
		if(test):
			lst.append('_test')
		if(mod):
			lst.append(f'{mod}{suffix}')
		return seq.join(lst)



from PyQt5.QtWidgets import QPushButton,QApplication
if __name__=='__main__':
	mt=XJ_ModTest()
	# mods=mt.Opt_LoadMods('Functions')
	# mods=mt.Opt_LoadMods('Structs')
	mods=mt.Opt_LoadMods('Widgets')
	print(len(mods))
	for mod in mods:
		print(mod['mTime'],mod['mod'])
	print('\n\n')



	app=QApplication([])
	btn=QPushButton('0')
	num=0
	def SetText(num):
		btn.setText(f'{num}: {mods[num]["mod"]}')
	def Test():
		global num
		print('\n')
		mt.Opt_TestMod(num)
		num=(num+1)%len(mods)
		SetText(num)
	SetText(num)
	btn.show()
	btn.resize(250,50)
	btn.clicked.connect(Test)

	exit(app.exec())





