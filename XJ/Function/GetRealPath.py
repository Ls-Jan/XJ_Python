

import os
import inspect

__all__=['GetRealPath']

def GetRealPath(relativePath):#用于获取绝对路径，调用者(脚本/模块)所在目录为根路径
	info=inspect.stack()[1]#调用者的上下文信息
	path=info.filename#本文件路径
	path=os.path.split(path)[0]#当前所在目录
	path=os.path.join(path,relativePath)#路径拼接
	path=os.path.realpath(path)#改成绝对路径
	return path

