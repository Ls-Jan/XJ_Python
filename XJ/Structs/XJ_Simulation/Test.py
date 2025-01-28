__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .XJ_Keyboard_Type1 import XJ_Keyboard_Type1,VirtualKey
from .XJ_Mouse_Type1 import XJ_Mouse_Type1
from time import sleep

#这个测试写得一坨狗屎，懒得搞了
__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		kbLst=[XJ_Keyboard_Type1()]
		msLst=[XJ_Mouse_Type1()]
		kbTest=[
			('Opt_Click("$")','单字符($)键入','A','B','C'),
			('Opt_Click($)','方向键(上下左右)键入',VirtualKey.Up,VirtualKey.Down,VirtualKey.Left,VirtualKey.Right),
			('Opt_TypeStr("$",1)','文本($)1秒键入','一二三'),
		]
		msTest=[
			('Get_Pos()',(None,'鼠标位置:$')),
			('Opt_Click($)','单键(左右)点击',1,2),
			('Opt_Move($)','鼠标移动(位置:$)',(500,500),(1000,500)),
			('Opt_Wheel($)','滚轮上下滚动(滚动量:$)',400,-200),
		]

		key=input('输入数字选择测试：键盘(1)、鼠标(2)、键鼠(任意)')
		print('3秒后开始执行')
		sleep(3)
		if(not(len(key)==1 and (key=='1' or key=='2'))):
			key='12'
		test=[(kbLst,kbTest,'【以下为按键模拟】') if k=='1' else (msLst,msTest,'【以下为鼠标模拟】') for k in key]
		for t in test:
			objs,tests,info=t
			print(info)
			for obj in objs:
				self.__Test(obj,tests)
			sleep(1)
		return super().Opt_Run()
	def __Test(self,obj,testLst):
		print(f'使用的类：{type(obj)}')
		for ts in testLst:
			info_before=None
			info_after=None
			i=ts[0].find('(')
			name_func=ts[0][:i]
			name_args=ts[0][i:]
			name_args=name_args if len(name_args)==2 else name_args[:-1]+',)'
			func=getattr(obj,name_func)
			print(">>>",name_args)
			if(type(ts[1])==tuple):
				info_before,info_after=ts[1]
			else:
				info_before=ts[1]
			if(info_before):
				print(info_before.replace('$',','.join([str(val) for val in ts[2:]])))
			for args in ts[2:]:
				args=eval(name_args.replace('$',str(args)))
				rst=func(*args)
				if(info_after):
					print(info_after.replace('$',rst))
			sleep(1)
		print()





