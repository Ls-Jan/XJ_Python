__version__='1.0.0'
__author__='Ls_Jan'
__all__=['XJQ_TextInputDialog']

from PyQt5.QtWidgets import QWidget,QTextEdit,QPushButton,QGridLayout
from PyQt5.QtGui import QShowEvent,QHideEvent
from PyQt5.QtCore import Qt,pyqtSignal,QObject,QEvent


class XJQ_TextInputDialog(QWidget):
	'''
		文本输入框，带有确认按钮。
		按下Alt+Enter可执行“确认”操作
	'''
	textSent=pyqtSignal(str)#发送文本
	def __init__(self,title:str='文本输入',parent:QWidget=None,*,tx:QTextEdit=None,btnOK:QPushButton=None):
		'''
			可指定具体的文本框控件tx和确认按钮控件btnOK
		'''
		super().__init__(parent)
		if(tx==None):
			tx=QTextEdit(self)
		if(btnOK==None):
			btnOK=QPushButton(self)
			btnOK.setText('确认')
		self.__tx=tx
		self.__ok=btnOK
		self.__dialogMode=True
		self.__hasSent=False

		grid=QGridLayout(self)
		grid.addWidget(tx,0,0,1,2)
		grid.addWidget(btnOK,1,1)
		tx.setAcceptRichText(False)#禁止富文本
		tx.setParent(self)
		btnOK.setParent(self)
		btnOK.clicked.connect(self.__SendText)
		tx.installEventFilter(self)#要拦截Alt+Enter按键
		self.setWindowTitle(title)
		self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint,False)#隐藏最大最小化按钮
		self.setWindowModality(Qt.WindowModality.ApplicationModal)#模态，屏蔽其他窗口
		self.Set_DialogMode(True)
	def Set_DialogMode(self,flag:bool):
		'''
			是否设置成弹窗模式。
			弹窗模式下：
				- 发送文本后自动关闭窗口；
				- 直接关闭窗口(不发送文本)会清空文本框；
			非弹窗模式与上面相反。
		'''
		self.__dialogMode=flag
		if(flag):
			self.setWindowFlag(Qt.WindowType.Dialog)#弹窗
		else:
			self.setWindowFlag(Qt.WindowType.Dialog,False)#取消弹窗弹窗
	def Set_Text(self,tx:str):
		'''
			设置文本框内容
		'''
		self.__tx.clear()
		self.__tx.append(tx)#使用该操作会顺带移动光标到文末，而setText仅会让光标停留原处
	def Get_TextEdit(self):
		'''
			获取文本输入框控件以进行更加细化的操作
		'''
		return self.__tx
	def Get_OKButton(self):
		'''
			获取确认按钮以进行更为细化的操作
		'''
		return self.__ok
	def __SendText(self):
		'''
			发送当前文本内容，信号为textSent
		'''
		if(not self.__hasSent):
			self.textSent.emit(self.__tx.toPlainText() if self.isVisible() else '')
			self.__hasSent=True
			if(self.__dialogMode):
				self.close()
	def showEvent(self,event:QShowEvent):
		self.__hasSent=False
		return super().showEvent(event)
	def hideEvent(self,event:QHideEvent):
		if(self.__dialogMode):
			self.__tx.clear()
		self.__SendText()
		return super().hideEvent(event)
	def eventFilter(self,obj:QObject,event:QEvent):
		if(event.type()==event.Type.KeyPress):#按键事件
			mod=event.modifiers()
			if(event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter):#按下回车键
				if(mod&Qt.KeyboardModifier.AltModifier):#按着ALT键
					self.__SendText()
					return True#已将该事件完成(拦截)，不向下传递
		return False#不做处理，交由下级完成



