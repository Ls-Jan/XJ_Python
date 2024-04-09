

from PyQt5.QtWidgets import QFrame,QLineEdit,QCompleter,QHBoxLayout
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QColor,QFont
from .XJQ_PureColorIconButton import XJQ_PureColorIconButton
from ..Functions.GetRealPath import GetRealPath

__all__=['XJQ_SearchBox']
class XJQ_SearchBox(QFrame):
	'''
		简单搜索框(无下拉列表)，样式仿照Bing的搜索框。
		
		信号commited:在回车或者点击搜索按钮时触发；
		信号updated:在搜索框内容发生变化时触发，在需要动态修改候选词列表时可使用该信号，同时也能将候选列表的长度控制在理想范围内(虽然没必要)
	'''
	commited=pyqtSignal(str)
	updated=pyqtSignal(str)

	styleSheet={
		'searchBox':'''
					.XJQ_SearchBox{
						background:#8888FF;
						border-radius: 12px; 
					}
				''',
		'standbyLst':'''
					QListView{
						background-color: #FFFFFF;
						color: #353637;
						selection-background-color: #3A72D8;
						selection-color: white;
						show-decoration-selected: 1;
						font-size: 14pt;
						font-family: microsoft yahei;
					}
					QScrollBar
					{
						background: rgba(255,255,255,5%);
						width: 6px;
					}
					QScrollBar::add-line {
						width:0;
						height:0;
					}
					QScrollBar::sub-line {
						width:0;
						height:0;
					}
					QScrollBar::handle {
						background: rgba(64,64,64,75%);
					}
					QScrollBar::sub-page {
						background: rgba(0,0,0,30%);
					}
					QScrollBar::add-page {
						background: rgba(0,0,0,30%);
					}						
				'''
	}

	def __init__(self,iconSearch:str=GetRealPath('../Icons/搜索.png'),iconClear:str=GetRealPath('../Icons/去除.png')):
		super().__init__()
		btnSearch=XJQ_PureColorIconButton(iconSearch)
		btnClear=XJQ_PureColorIconButton(iconClear)
		input=QLineEdit()
		comp=QCompleter([])

		input.setCompleter(comp)
		btnSearch.Set_FgColor(pressed=QColor(224,224,224,224))#让颜色变化不那么大
		input.textChanged.connect(self.__CB_TextChange)
		input.returnPressed.connect(self.__CB_Commit)
		btnSearch.clicked.connect(self.__CB_Commit)
		btnClear.clicked.connect(self.__CB_TextClear)
		btnClear.hide()
		input.setStyleSheet('''
					background:transparent;
					border-width:0;
					border-style:outset
					''')

		hbox=QHBoxLayout(self)
		hbox.addWidget(btnSearch)
		hbox.addWidget(input)
		hbox.addWidget(btnClear)
		hbox.setContentsMargins(8,8,8,8)
		hbox.setSpacing(0)

		self.__input=input
		self.__btnSearch=btnSearch
		self.__btnClear=btnClear
		self.Set_Size(14)
		self.Set_StyleSheet(self.styleSheet)
	def Set_StyleSheet(self,styleSheet:dict):
		'''
			设置样式表，内容参考XJQ_SearchBox.styleSheet
		'''
		self.styleSheet=styleSheet
		# 设置QCompleter样式：https://blog.csdn.net/hellokandy/article/details/128844511
		self.__input.completer().popup().setStyleSheet(self.styleSheet['standbyLst'])
		self.setStyleSheet(self.styleSheet['searchBox'])
	def Set_StandbyList(self,lst:list=None,matchMode:Qt.MatchFlag=None):
		'''
			设置候选词列表以及候选词匹配模式，
			匹配模式通常使用Qt.MatchFlag.MatchStartsWith(匹配开头)和Qt.MatchFlag.MatchContains(匹配包含)
		'''
		comp=self.__input.completer()
		if(lst!=None):
			model=comp.model()
			diff=model.rowCount()-len(lst)
			model.removeRows(0,diff)
			model.insertRows(0,-diff)
			for i in range(len(lst)):
				model.setData(model.index(i),lst[i])
		if(matchMode!=None):
			#设置匹配模式：https://juejin.cn/post/7155268553950625806#heading-1
			comp.setFilterMode(matchMode)
	def Set_Size(self,height:int=10):
		'''
			设置搜索框大小
		'''
		fontHeight=height
		iconHeight=height+10
		selfHeight=height+26
		self.__input.setFont(QFont(self.__input.font().family(),fontHeight))
		self.__btnSearch.resize(iconHeight,iconHeight)
		self.__btnClear.resize(iconHeight-4,iconHeight-4)
		self.setFixedHeight(selfHeight)
	def Set_Font(self,font:QFont):
		'''
			设置搜索框字体(同时设置搜索框大小)
		'''
		self.__input.setFont(font)
		self.Set_Size(font.pixelSize())
	def Set_Focus(self,reason:Qt.FocusReason=None):
		'''
			将焦点引到搜索框中
		'''
		reason=[reason] if reason else []
		self.__input.setFocus(*reason)
	def __CB_TextChange(self):
		tx=self.__input.text().strip()
		self.updated.emit(tx)
		self.__btnClear.show() if tx else self.__btnClear.hide()
	def __CB_TextClear(self):
		self.__btnClear.hide()
		self.__input.blockSignals(True)
		self.__input.clear()
		self.__input.setFocus()
		self.__input.blockSignals(False)
	def __CB_Commit(self):
		self.commited.emit(self.__input.text().strip())




