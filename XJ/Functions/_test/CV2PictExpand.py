

from ..CV2PictExpand import CV2PictExpand
from ..GetRealPath import GetRealPath
from ..CV2LoadPict import CV2LoadPict
import cv2

if True:
	im=CV2LoadPict(GetRealPath('../../Icons/云下载.png'))
	imNew=CV2PictExpand(im)
	cv2.imshow("Image",imNew)
	cv2.waitKey()
	exit()
