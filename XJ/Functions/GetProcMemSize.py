
import os
import psutil

__all__=['GetProcMemSize']
def GetProcMemSize(pid=None):
	'''
		获取进程的内存占用情况(用于特殊场合防止内存爆炸)，单位MB
	'''
	if(not pid):
		pid=os.getpid()
	process = psutil.Process(pid)
	memInfo = process.memory_info()
	return memInfo.rss / 1024 / 1024
