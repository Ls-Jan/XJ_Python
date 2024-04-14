
__version__='1.1.0'
__author__='Ls_Jan'

from .XJQ_Slider import XJQ_Slider
from ...ModuleTest import XJQ_Test

import sys
from PyQt5.QtWidgets import QVBoxLayout,QWidget
from PyQt5.QtCore import Qt

__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()
		slider=XJQ_Slider()

		slider.setOrientation(Qt.Horizontal)
		slider.valueChanged.connect(lambda value:print(value))
		slider.sliderPressed.connect(lambda :print("PRESS"))
		slider.sliderReleased.connect(lambda :print("RELEASE"))
		slider.setInvertedControls(False)#看我找到了什么？
		slider.setInvertedAppearance(False)#看我找到了什么？
		# slider.setInvertedControls(True)
		# slider.setInvertedAppearance(True)
		# slider.Set_HandleWidth(50)
		# slider.setMaximum(0)
		# slider.setMaximum(41)
		slider.setMaximum(5)
		slider.setMaximum(50)
		# slider.setMaximum(5000000)
		# slider.setValue(25)
		slider.setValue(extra=40)

		win=QWidget()
		win.setStyleSheet('background:#222222')
		vbox=QVBoxLayout(win)
		vbox.addWidget(slider)

		self.__win=win
	def Opt_Run(self):
		self.__win.resize(700,400)
		self.__win.show()
		return super().Opt_Run()

