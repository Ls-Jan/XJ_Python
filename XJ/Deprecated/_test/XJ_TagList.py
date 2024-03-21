from ..XJ_TagList import *

if True:
	lst=XJ_TagList(tagList=['groupID','checkStatus'])
	lst.Opt_Insert(count=1000000,groupID=0,checkStatus=1)
	lst.Opt_Delete(4,55)

	lst.Opt_Insert(count=100,groupID=1,checkStatus=1)
	rst=lst.Get_RowTags()
	print(rst)
	rst=lst.Get_Length(groupID=0)
	# rst=lst.Get_Length(groupID=1)
	# rst=lst.Get_Length()
	print(rst)

