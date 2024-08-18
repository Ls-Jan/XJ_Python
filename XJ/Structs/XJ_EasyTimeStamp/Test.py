__version__='1.1.0'
__author__='Ls_Jan'
__all__=['Test']

from ...ModuleTest import XJ_Test
from .XJ_EasyTimeStamp import XJ_EasyTimeStamp
import random

class Test(XJ_Test):
	def Opt_Run(self):
		ts=XJ_EasyTimeStamp()
		ts.Opt_AddTimeStamp('Total')

		ts.Opt_AddTimeStamp()
		lst=[random.randint(1,100) for i in range(1000000)]
		print(f'创建列表：{round(ts.Get_DurationTime(),2)}s')

		ts.Opt_AddTimeStamp()
		lst=lst*100
		print(f'列表复制：{round(ts.Get_DurationTime(),2)}s')

		ts.Opt_AddTimeStamp()
		s=str(lst)
		print(f'字串化：{round(ts.Get_DurationTime(),2)}s')

		ts.Opt_AddTimeStamp()
		h=hash(s)
		print(f'哈希计算：{round(ts.Get_DurationTime(),2)}s')

		print(f'总用时：{round(ts.Get_DurationTime("Total"),2)}s')

		return super().Opt_Run()


