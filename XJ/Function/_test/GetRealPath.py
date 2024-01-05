from ..GetRealPath import *

import os

if True:
	p0=os.path.split(__file__)[0]
	p1='../GetRealPath.py'
	p2=GetRealPath(p1)
	print('    RootPath: ',p0)
	print('RelativePath: ',p1)
	print('AbsolutePath: ',p2)
	print()
