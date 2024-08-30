__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .XJ_KeyboardStatusHook import XJ_KeyboardStatusHook
from .XJ_MouseStatusHook import XJ_MouseStatusHook
from PyHook3 import HookConstants


__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):

		print("状态K0：按下A后进入状态K1，按下D后进入状态K2(退出)；")
		print("状态K1：按下S后进入状态K0，按下D后进入状态K2(退出)；")
		print()
		print("左键按下：进入状态M1")
		print("左键抬起：进入状态M0")
		print("右键按下：退出")
		print()
		print()

		ksk=XJ_KeyboardStatusHook(
			(0,ord('A'),1),
			(1,ord('S'),0),
			(0,ord('D'),2),
			(1,ord('D'),2))
		ksk.Opt_Start()
		ksk.Set_Callback({0:lambda event:print("KeyPress",event.GetKey()),1:lambda event:print("KeyPress",event.GetKey()),2:lambda event:ksk.Opt_Stop()})

		msk=XJ_MouseStatusHook(
			(0,HookConstants.WM_LBUTTONDOWN,1),
			(0,HookConstants.WM_RBUTTONDOWN,2),
			(1,HookConstants.WM_LBUTTONUP,0))
		msk.Set_Callback({0:lambda event:print("ButtonRelease"),1:lambda event:print("LeftPress"),2:lambda event:msk.Opt_Stop()})
		msk.Opt_Start()

		msk.Opt_Join()
		ksk.Opt_Join()
		return super().Opt_Run()


