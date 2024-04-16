
__version__='1.0.0'
__author__='Ls_Jan'

from PyQt5.QtWidgets import QAbstractItemView

__all__=['GetQItemViewShowingIndices']
def GetQItemViewShowingIndices(view:QAbstractItemView,extend=0):
	'''
		字面意思，就是获取QListView列表中，当前显示行的起始结束索引。
		extend对上下限额外修正，例如当前显示的是(3,12)，指定extend=5的话将返回(0,17)
	'''
	# 参考：https://cloud.tencent.com/developer/ask/sof/779490
	minRow=0
	maxRow=view.model().rowCount()-1
	rect = view.viewport().contentsRect()
	top = view.indexAt(rect.topLeft())
	bottom = view.indexAt(rect.bottomLeft())
	top=top.row() if top.isValid() else minRow
	bottom=bottom.row() if bottom.isValid() else maxRow
	top=max(minRow,top-extend)
	bottom=min(maxRow,bottom+extend)
	return top,bottom


