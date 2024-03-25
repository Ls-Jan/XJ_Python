
__version__='1.0.0'
__author__='Ls_Jan'

from ..Structs.XJ_GroupList import XJ_GroupList
from ..Structs.XJQ_PictLoader import XJQ_PictLoader
from ..Structs.XJQ_ItemViewPlugin.LoadingAnimation import LoadingAnimation
from ..Structs.XJQ_ItemViewPlugin.RowSourceManager import RowSourceManager
from ..Functions.GetRealPath import GetRealPath
from ..Functions.CV2ToQPixmap import CV2ToQPixmap
from .XJQ_MouseTriggerBox import XJQ_MouseTriggerBox
from .XJQ_HintBox import XJQ_HintBox#可以用QMenu替代，但写都写了，不用就感觉浪费

import re
from PyQt5.QtWidgets import QWidget,QListView,QLabel,QHBoxLayout
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QCursor,QIcon
from PyQt5.QtCore import QSize,QPoint,Qt


__all__=['XJQ_PictListView']
class XJQ_PictListView(QWidget):
	'''
		依赖XJ_Frame。
		专用于图标加载显示的列表控件，自带资源动态加载释放功能，鼠标悬停还能显示放大的图片。

		列表中的数据只允许通过Opt_Insert和Opt_Remove函数进行操作(不然会造成数据不同步甚至程序崩溃)。
	'''
	config={
		'iconSize':(64,64),#图标大小
		'cacheMax':200,#最大缓存数
		'cacheRetention':60,#缓存留存时长(s)
		'delayLoad':0.1,#延时加载(s)，列表停留不动一小段时间才开始加载图标
		'hintSize':(1000,600),#鼠标悬停时的图片放大预览
		'textFormat':'$path{val}$repeat{[val]}$index{-val}',#文本格式
	}

	class __TextFormat:
		'''
			用于文本格式化，与self.config['textFormat']有关
		'''
		__text=None
		__patterns=None
		def __init__(self,text:str='')->None:
			self.__text=''
			self.__patterns={}
			self.Set_Format(text)
		def Set_Format(self,text:str)->None:
			if(text):
				patterns={'path':'val','repeat':'val','index':'val'}
				for key in patterns:
					pat=f'\${key}{{(.+?)}}'
					val=re.findall(pat,text)
					if(val):
						patterns[key]=val[0]
					text=re.sub(pat,f'${key}',text)
				self.__text=text
				self.__patterns=patterns
		def Get_Text(self,path:str,repeat:str,index:str)->str:
			vals={'path':path,'repeat':repeat,'index':index}
			text=self.__text
			patterns=self.__patterns
			for key in patterns:
				val=vals[key]
				val=patterns[key].replace('val',val) if val else ''
				text=text.replace(f'${key}',val)
			return text
	def __init__(self,*args,loadingGIF=GetRealPath('../Icons/Loading/加载动画-1.gif')):
		super().__init__(*args)
		lv=QListView(self)
		lvLA=LoadingAnimation(view=lv)
		lvSM=RowSourceManager(view=lv)
		lvModel=QStandardItemModel(lv)
		pl=XJQ_PictLoader()
		mt=XJQ_MouseTriggerBox()
		hb=XJQ_HintBox(QLabel())
		QHBoxLayout(mt).addWidget(lv)
		mt.setParent(self,True)
		mt.Opt_AddArea('ListView',lv)
		mt.hover.connect(self.__HoverShow)
		pl.loaded.connect(self.__IconSet)
		lv.setModel(lvModel)
		lvSM.rowShowChanged.connect(self.__IconChanged)
		lvSM.Set_RowExtend(0)
		lvLA.Set_LoadingGIF(loadingGIF)

		self.config=self.config.copy()
		self.__visibleRowLst=[]
		self.__lv=lv
		self.__lvSM=lvSM
		self.__lvLA=lvLA
		self.__pl=pl
		self.__hb=hb
		self.__checkable=True
		self.__frameLst=XJ_GroupList()
		self.__lvModel=lvModel
		self.__textFormat=self.__TextFormat(self.config['textFormat'])
		self.__showCheckOnly=False
		self.__showGroupOnly=set()
		self.Opt_ReloadConfig()
	def Get_CursorRow(self,pos:QPoint=QPoint()):
		'''
			获取坐标对应的行，传入的是全局坐标。
			如果pos无效那么将以当前鼠标坐标为准
		'''
		if(pos.isNull()):
			pos=QCursor.pos()
		pos=self.__lv.mapFromGlobal(pos)
		return self.__lv.indexAt(pos)
	def Get_VisibleRow(self):
		'''
			获取可见的行，返回行索引列表
		'''
		return self.__visibleRowLst
	def Get_CheckedRow(self,checked:bool=True,returnFrame:bool=False):
		'''
			返回被选中的索引列表。
			如果checked为假则返回未被选中的行。
			如果returnIndices为真那么将返回对应图片数据(XJ_Frame)。
		'''
		result=[]
		lvModel=self.__lvModel
		flag=Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
		for i in range(lvModel.rowCount()):
			if(lvModel.item(i).checkState()==flag):
				result.append(self.__frameLst.Get_ItemData(i) if returnFrame else i)
		return result
	def Get_ListView(self):
		'''
			返回QListView控件，以便进行更为细化的操作
		'''
		return self.__lv
	def Get_Length(self):
		'''
			获取列表长度
		'''
		return len(self.__frameLst)
	def Get_GroupName(self):
		'''
			获取分组的名称，返回{<str>:<str>}，含义是{分组：组名}
		'''
		rst={}
		for group,info in self.__frameLst.Get_GroupsInfo().items():
			rst[group]=info['name']
		return rst
	def Get_GroupCount(self):
		'''
			获取分组的组个数信息，返回{<str>:{<int>:<int>}}，含义是{分组：{子分组：数量}}
		'''
		rst={}
		for group,info in self.__frameLst.Get_GroupsInfo().items():
			rst[group]={}
			for subGroup,subInfo in info['subGroup'].items():
				rst[group][subGroup]=subInfo['count']
		return rst
	def Set_GroupName(self,group:str,name:str):
		'''
			设置分组对应的名称
		'''
		self.__frameLst.Set_GroupName((group,),name)
		self.Opt_UpdateText()
	def Set_Checkable(self,flag:bool):
		'''
			设置是否显示复选框
		'''
		if(self.__checkable!=flag):
			lvModel=self.__lvModel
			for i in range(lvModel.rowCount()):
				lvModel.item(i).setCheckable(flag)
			self.__checkable=flag
	def Set_CheckState(self,*indices:int,check:bool):
		'''
			设置指定行的选中状态
		'''
		lvModel=self.__lvModel
		for index in indices:
			if(0<=index<lvModel.rowCount()):
				lvModel.item(index).setCheckState(Qt.CheckState.Checked if check else Qt.CheckState.Unchecked)
	def Set_VisibleGroup(self,*groups,showAll:bool=False):
		'''
			设置仅指定分组可见。groups格式为(<str>,<int>)，传入信息为(分组，子分组)
		'''
		self.__showGroupOnly.clear()
		if(showAll):
			for group,info in self.Get_GroupCount().items():
				self.__showGroupOnly.update(((group,subGroup) for subGroup in info))
		else:
			self.__showGroupOnly.update(groups)
		self.__SetVisibleRow()
	def Set_VisibleCheckedRow(self,flag:bool):
		'''
			设置仅被选中的行可见。如果flag为真则全部显示
		'''
		if(flag):
			self.__showCheckOnly=False
		else:
			self.__showCheckOnly=True
		self.__SetVisibleRow()
	def Set_LoadingGIF(self,path:str=None,msec:int=None):
		'''
			设置GIF加载动图以及刷新间隔
		'''
		self.__lvLA.Set_LoadingGIF(path,msec)
	def Opt_Insert(self,frameLst:list,group:str,groupName:str='',index:int=-1,subGroup:int=-1):
		'''
			向列表指定位置插入数据，返回插入数据所属的组id。
			frameLst为XJ_Frame列表，
			index为负值则添加到末尾。
			group为frameLst所属的分组，
			subGroup为负值则新增一个子分组。
			如果group已存在那么groupName不生效。
		'''
		if(index<0):
			index=len(self.__frameLst)
		self.__pl.Opt_Remove(*list(range(index,len(self.__frameLst))))#把index后面的任务全部清掉
		self.__lvSM.Opt_ListChange(index,len(frameLst),insert=True)
		for f in reversed(frameLst):
			item=QStandardItem()
			item.setData(True,self.__lvLA.loadingRole)
			item.setCheckable(self.__checkable)
			item.setCheckState(Qt.CheckState.Checked)
			item.setEditable(False)
			self.__lvModel.insertRow(index,item)
		if(subGroup>0):
			self.__frameLst.Opt_Insert(*frameLst,index=index,group=(group,subGroup),subGroup=False)
		else:
			self.__frameLst.Opt_Insert(*frameLst,index=index,group=(group,))
		self.__showGroupOnly.add((group,subGroup))
		if(len(self.Get_GroupCount()[group])==1):
			if(groupName):
				self.__frameLst.Set_GroupName((group,),groupName)
		self.Opt_UpdateText()#直接无脑全更新
		self.__UpdateVisibleRowLst()
		self.update()
	def Opt_Remove(self,index:int,count:int):
		'''
			移除指定数据。
			如果count为负值则视为列表长度
		'''
		if(count<0):
			count=len(self.__frameLst)
		self.__pl.Opt_Remove(*list(range(index,index+count)))#先清空指定任务
		self.__frameLst.Opt_Remove(start=index,count=count)
		self.__lvModel.removeRows(index,count)
		self.__lvSM.Opt_ListChange(index,count,remove=True)
		self.__UpdateVisibleRowLst()
	def Opt_Clear(self):
		'''
			清除列表
		'''
		self.Opt_Remove(0,-1)
	def Opt_ReloadConfig(self,keys=[]):
		'''
			重新加载相关配置。
			如果指定关键词则只加载对应配置，否则将全部加载一遍
		'''
		lv=self.__lv
		lvSM=self.__lvSM
		lvLA=self.__lvLA
		if(len(keys)==0):
			keys=self.config.keys()
		for key in keys:
			if(key in self.config):
				val=self.config[key]
				if(key=='iconSize'):
					lv.setIconSize(QSize(*val))
				elif(key=='delayLoad'):
					lvSM.Set_DelayTime(val)
				elif(key=='cacheMax'):
					lvSM.Set_RowCountMax(val)
				elif(key=='cacheRetention'):
					lvSM.Set_RetentionTime(val)
				elif(key=='textFormat'):
					self.__textFormat.Set_Format(val)
					self.Opt_UpdateText()
	def Opt_UpdateText(self,indices=None):
		'''
			indices为可遍历对象，记录着列表索引值。
			重新加载指定索引项的对应文本，当某项对应的XJ_Frame的name发生变动时需调用该函数以进行文本更新。
			如果indices为None则重新加载所有索引项(代价或许有点大？不是很清楚QStandardItem.setText的性能影响)
		'''
		if(indices==None):
			indices=range(len(self.__frameLst))
		record={}
		for group,info in self.__frameLst.Get_GroupsInfo().items():
			multiple=len(info['subGroup'])>1
			for subGroup,subInfo in info['subGroup'].items():
				record[(group,subGroup)]=(info['name'],subInfo['count'],multiple)
		for i in indices:
			f=self.__frameLst.Get_ItemData(i)
			group=self.__frameLst.Get_ItemGroup(i,False)
			text=self.__textFormat.Get_Text(record[group][0],str(group[1]) if record[group][2] else '',f.hint())
			self.__lvModel.item(i).setText(text)
		self.update()
	def __HoverShow(self,name:str,flag:bool):
		'''
			该函数与XJQ_MouseTriggerBox绑定，鼠标悬浮时显示放大的图片
		'''
		if(flag):
			lv=self.__lv
			p0=QCursor().pos()
			p1=lv.mapFromGlobal(p0)
			index=lv.indexAt(p1).row()
			if(index>=0):
				pix=CV2ToQPixmap(self.__frameLst.Get_ItemData(index).data(self.config['hintSize'],allowScale=False))
				lb=self.__hb.Get_Content()
				lb.resize(pix.size())
				lb.setPixmap(pix)
				self.__hb.update()
		else:
			self.__hb.hide()
	def __IconChanged(self,indices,show)->None:
		'''
			与RowSourceManager绑定，用于加载释放图标的图片资源
		'''
		if(show):
			self.__pl.Opt_Append(*[(i,self.__frameLst.Get_ItemData(i),self.config['iconSize'],False) for i in indices])
		else:
			for index in indices:
				self.__IconSet(index,None,True)
	def __IconSet(self,id,pix,loading=False):
		'''
			该函数与XJQ_PictLoader绑定，设置列表图标，以及单元格的加载状态
		'''
		#QStandardItem::setData源码：https://codebrowser.dev/qt5/qtbase/src/gui/itemmodels/qstandarditemmodel.cpp.html#_ZN13QStandardItem7setDataERK8QVarianti
		self.__lvModel.blockSignals(True)#因为QStandardItem的数据操作会发送itemChanged信号，不予屏蔽的话会对UI界面造成显著卡顿
		item=self.__lvModel.item(id)
		item.setIcon(QIcon(pix))
		item.setData(loading,self.__lvLA.loadingRole)
		self.__lvModel.blockSignals(False)
	def __SetVisibleRow(self):
		'''
			设置可见行
		'''
		self.__visibleRowLst.clear()
		for i in range(len(self.__frameLst)):
			group=self.__frameLst.Get_ItemGroup(i,False)
			item=self.__lvModel.item(i)
			visible=False
			if(group in self.__showGroupOnly):
				if(not self.__showCheckOnly or item.checkState()==Qt.CheckState.Checked):
					self.__visibleRowLst.append(i)
					visible=True
			self.__lv.setRowHidden(i,not visible)
	def __UpdateVisibleRowLst(self):
		'''
			更新visibleRowLst数据
		'''
		self.__visibleRowLst=[i for i in range(len(self.__frameLst)) if not self.__lv.isRowHidden(i)]

