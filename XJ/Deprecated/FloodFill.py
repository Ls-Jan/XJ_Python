#洪水填充代码，从边框填起
#因为没多少用途就舍弃掉了

import cv2
import numpy as np

def Trans_WidMask_Style(pict:np.ndarray):
	#洪填，将外围填充
	arr=cv2.cvtColor(pict,cv2.COLOR_RGBA2GRAY)
	h, w = arr.shape[:2]
	mask = np.zeros([h+2, w+2],np.uint8)
	arr_copy=arr.copy()
	arr=cv2.rectangle(arr,(0,0),(w-1,h-1),(int(arr[0][0]),))
	cv2.floodFill(arr, mask, (0,0), (0,), (2,), (2,), cv2.FLOODFILL_FIXED_RANGE)#参数是试出来的...懒得研究洪填
	arr=arr==arr_copy
	arr=arr*255
	arr=arr.astype(np.uint8)
	return arr

