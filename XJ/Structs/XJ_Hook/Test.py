__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .XJ_Hook import XJ_Hook
from PyHook3 import HookConstants


__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):

		print("状态K0：按下A后进入状态K1，按下S后进入状态K2(退出)；")
		print("状态K1：按下D后进入状态K0，按下S后进入状态K2(退出)；")
		print()
		print("左键按下：进入状态M1")
		print("左键抬起：进入状态M0")
		print("右键按下：退出")
		print()
		print()

		hk=XJ_Hook()

		hk.Set_Trans(0,ord('A'),1,True)
		hk.Set_Trans(1,ord('D'),0,True)
		hk.Set_KeyAction(ord('S'),lambda stat,key:(2,hk.Opt_Stop())[0],True)
		hk.Set_StatAction(0,lambda stat:print(f'K{stat}'),False)
		hk.Set_StatAction(1,lambda stat:print(f'K{stat}'),False)

		hk.Set_Trans(0,HookConstants.WM_LBUTTONDOWN,1)
		hk.Set_Trans(1,HookConstants.WM_LBUTTONUP,0)
		hk.Set_KeyAction(HookConstants.WM_RBUTTONDOWN,lambda stat,key:(2,hk.Opt_Stop())[0],None)
		hk.Set_StatAction(0,lambda stat:print(f'M{stat}'),True)
		hk.Set_StatAction(1,lambda stat:print(f'M{stat}'),True)

		hk.Opt_Start()
		hk.Opt_Join()

		return super().Opt_Run()


