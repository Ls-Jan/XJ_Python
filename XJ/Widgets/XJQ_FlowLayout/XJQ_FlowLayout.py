
__version__='1.0.1'
__author__='Ls_Jan'

from PyQt5.QtCore import QPoint, QRect, QSize, Qt,pyqtSignal
from PyQt5.QtWidgets import QLayout, QPushButton, QSizePolicy, QWidget,QSpacerItem

__all__=['XJQ_FlowLayout']

#他人实现的流式布局，这里就不自己实现了(换句话说下面的代码是copy别人的)
#原代码链接：https://www.jianshu.com/p/dbccfac62626
class XJQ_FlowLayout(QLayout):
	"""流式布局,使用说明
	1.声明流式布局 layout = FlowLayout
	2.将元素放入流式布局中
	3.将QGroupBox应用流式布局
	4.如果期望水平流式,将QGroupBox放入到QHBoxLayout,如果期望垂直布局,将QGroupBox放入到QVBoxLayout

	- 使用addWidget、removeWidget以添加/移除控件
	- 在出现卡顿时可调用blockSignals
	- 可调用update以更新布局
	"""
	__block=False
	heightChanged = pyqtSignal(int)
	def __init__(self, parent=None, margin=0, spacing=-1):
		super().__init__(parent)
		if parent is not None:
			self.setContentsMargins(margin, margin, margin, margin)
		self.setSpacing(spacing)

		self._item_list = []
	def __del__(self):
		while self.count():
			self.takeAt(0)
	def Get_WidgetLst(self,start:int=0,count:int=-1):
		'''
			返回控件列表
		'''
		if(count<0):
			count=len(self._item_list)
		stop=start+count
		lst=self._item_list[start:] if start<0 and stop>=0 else self._item_list[start:stop]
		return list(map(lambda item:item.widget(),lst))
	def addItem(self, item):  # pylint: disable=invalid-name
		self._item_list.append(item)
	def addSpacing(self, size):  # pylint: disable=invalid-name
		self.addItem(QSpacerItem(size, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
	def count(self):
		return len(self._item_list)
	def itemAt(self, index):  # pylint: disable=invalid-name
		if 0 <= index < len(self._item_list):
			return self._item_list[index]
		return None
	def takeAt(self, index):  # pylint: disable=invalid-name
		if 0 <= index < len(self._item_list):
			return self._item_list.pop(index)
		return None
	def expandingDirections(self):  # pylint: disable=invalid-name,no-self-use
		return Qt.Orientations(Qt.Orientation(0))
	def hasHeightForWidth(self):  # pylint: disable=invalid-name,no-self-use
		return False#不觉得自动调高有什么用处，而且还会出现频繁调用heighForWidth的情况
		# return True
	def heightForWidth(self, width):  # pylint: disable=invalid-name
		height = self._do_layout(QRect(0, 0, width, 0), True)
		return height
	def setGeometry(self, rect):  # pylint: disable=invalid-name
		'''
			在设置blockSignals(True)时该函数调用不生效
		'''
		if(not self.__block):
			super().setGeometry(rect)
			self._do_layout(rect, False)
	def sizeHint(self):  # pylint: disable=invalid-name
		return self.minimumSize()
	def blockSignals(self,flag:bool):
		'''
			屏蔽信号，尤其是在布局内的控件频繁更新(例如设置显隐)时调用，以减少不必要的函数调用
		'''
		self.__block=flag
		return super().blockSignals(flag)
	def minimumSize(self):  # pylint: disable=invalid-name
		height=self._do_layout(self.geometry(), True)
		size = QSize()

		for item in self._item_list:
			minsize = item.minimumSize()
			extent = item.geometry().bottomRight()
			size = size.expandedTo(QSize(minsize.width(), extent.y()))

		size.setHeight(height)
		margin=self.contentsMargins()
		size += QSize(margin.left()+margin.right(),margin.top()+margin.bottom())
		return size
	def _do_layout(self, rect, test_only=False):
		m = self.contentsMargins()
		effective_rect = rect.adjusted(+m.left(), +m.top(), -m.right(), -m.bottom())
		x = effective_rect.x()
		y = effective_rect.y()
		line_height = 0
		for item in self._item_list:
			wid = item.widget()
			if(wid is None or wid.isVisible()==False):#隐藏控件不占位
				continue
			space_x = self.spacing()
			space_y = self.spacing()
			if wid is not None:
				space_x += wid.style().layoutSpacing(
					QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
				space_y += wid.style().layoutSpacing(
					QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

			next_x = x + item.sizeHint().width() + space_x
			if next_x - space_x > effective_rect.right() and line_height > 0:
				x = effective_rect.x()
				y = y + line_height + space_y
				next_x = x + item.sizeHint().width() + space_x
				line_height = 0

			if not test_only:
				item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

			x = next_x
			line_height = max(line_height, item.sizeHint().height())
		new_height = y + line_height - rect.y()
		self.heightChanged.emit(new_height)
		return new_height

