
__version__='1.0.0'
__author__='Ls_Jan'
__all__=['_Node']

from typing import List

class _Node:
	x:int=0#左
	y:int=0#上
	w:int=0#宽
	h:int=0#高
	cw:int=0#列最大宽(根据当前对齐情况而变化)
	nodeID_parent:int=-1#父节点
	nodeID_children:List[int]#子节点列表
	node_isVisible:int=1#可见等级。完全可见(1)、仅隐去子节点(0)、本节点及子节点不可见(-1)

	def __init__(self,w:int,h:int,parent:int=-1):
		self.nodeID_children=[]
		self.w=w
		self.h=h
		self.nodeID_parent=parent


