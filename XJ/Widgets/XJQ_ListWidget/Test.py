
__version__='1.1.0'
__author__='Ls_Jan'

from ...ModuleTest import XJQ_Test
from .XJQ_ListWidget import XJQ_ListWidget
from ..XJQ_ListWidgetItem import XJQ_ListWidgetItem

from PyQt5.QtGui import QColor
__all__=['Test']
class Test(XJQ_Test):
	def __init__(self):
		super().__init__()

		lst=[
			QColor(255,160,0,128),
			QColor(255,0,0,128),
			QColor(0,0,255,128),
			QColor(255,160,0,128),
			QColor(0,0,255,128),
		]

		lv=XJQ_ListWidget()
		lst=[XJQ_ListWidgetItem(str(i),[f'标签{j}' for j in range(i%5+1)],lst[i%5]) for i in range(16)]
		for wid in lst:
			lv.Opt_AppendWidget(wid)
		# lv.Opt_RemoveRow(0)
		# lv.Opt_Clear()
		# print(lv.count())
		lv.setCurrentIndex(lv.model().index(3,0))
		lv.setCurrentIndex(lv.model().index(-1,0))
		lv.Opt_RemoveRow(4)
		lv.indexWidget(lv.model().index(1,0)).Opt_Change(title="AAAAAAAAAAA")
		lv.currentRowChanged.connect(lambda row:print(row,lv.currentIndex()))
		self.__lv=lv

	def Opt_Run(self):
		self.__lv.show()
		return super().Opt_Run()

