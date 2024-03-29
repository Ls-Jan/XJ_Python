
__version__='1.0.0'
__author__='Ls_Jan'

import cv2
import numpy as np

__all__=['DrawRoundedRect']
def DrawRoundedRect(src:np.ndarray, top_left:tuple, bottom_right:tuple, radius:int=1, color:tuple=(255,), thickness:int=1, line_type=cv2.LINE_AA):
	'''
		用于补充cv2的圆角矩形绘制功能
		代码是copy他人的，镜像站：https://cloud.tencent.com/developer/ask/sof/100455675
	'''
	#  corners:
	#  p1 - p2
	#  |     |
	#  p4 - p3

	p1 = top_left
	p2 = (bottom_right[1], top_left[1])
	p3 = (bottom_right[1], bottom_right[0])
	p4 = (top_left[0], bottom_right[0])

	height = abs(bottom_right[0] - top_left[1])

	if radius > 1:
		radius = 1

	corner_radius = int(radius * (height/2))

	if thickness < 0:

		#big rect
		top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
		bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

		top_left_rect_left = (p1[0], p1[1] + corner_radius)
		bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

		top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
		bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

		all_rects = [
		[top_left_main_rect, bottom_right_main_rect], 
		[top_left_rect_left, bottom_right_rect_left], 
		[top_left_rect_right, bottom_right_rect_right]]

		[cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

	# draw straight lines
	cv2.line(src, (p1[0] + corner_radius, p1[1]), (p2[0] - corner_radius, p2[1]), color, abs(thickness), line_type)
	cv2.line(src, (p2[0], p2[1] + corner_radius), (p3[0], p3[1] - corner_radius), color, abs(thickness), line_type)
	cv2.line(src, (p3[0] - corner_radius, p4[1]), (p4[0] + corner_radius, p3[1]), color, abs(thickness), line_type)
	cv2.line(src, (p4[0], p4[1] - corner_radius), (p1[0], p1[1] + corner_radius), color, abs(thickness), line_type)

	# draw arcs
	cv2.ellipse(src, (p1[0] + corner_radius, p1[1] + corner_radius), (corner_radius, corner_radius), 180.0, 0, 90, color ,thickness, line_type)
	cv2.ellipse(src, (p2[0] - corner_radius, p2[1] + corner_radius), (corner_radius, corner_radius), 270.0, 0, 90, color , thickness, line_type)
	cv2.ellipse(src, (p3[0] - corner_radius, p3[1] - corner_radius), (corner_radius, corner_radius), 0.0, 0, 90,   color , thickness, line_type)
	cv2.ellipse(src, (p4[0] + corner_radius, p4[1] - corner_radius), (corner_radius, corner_radius), 90.0, 0, 90,  color , thickness, line_type)

	return src


