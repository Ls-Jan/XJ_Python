__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJ_Test
from .DrawRoundedRect import DrawRoundedRect
import numpy as np
import cv2


__all__=['Test']
class Test(XJ_Test):
	def Opt_Run(self):
		top_left = (0, 0)
		bottom_right = (500, 800)
		color = (255, 255, 255)
		image_size = (500, 800, 4)
		img = np.zeros(image_size)
		DrawRoundedRect(img, top_left, bottom_right, color=color, radius=0.5, thickness=-1)

		cv2.imshow('rounded_rect', img)
		cv2.waitKey(0)
		return super().Opt_Run()
