# XJQ_FlowLayout

他人实现的流式布局，这里就不自己实现了

原代码链接：https://www.jianshu.com/p/dbccfac62626

![XJQ_FlowLayout](../pict/XJQ_FlowLayout.gif)

``` py

from XJ.Widgets import XJQ_FlowLayout 
from XJ.Widgets import XJQ_Tag

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if True:
	app = QApplication(sys.argv)

	wid=QWidget()
	fbox=XJQ_FlowLayout()
	for i in range(10):
		fbox.addWidget(XJQ_Tag(None,str(i)*i+'\n'*(i%2)))
	wid.setMinimumHeight(100)
	wid.setLayout(fbox)
	wid.show()
	# fbox.heightChanged.connect(lambda h:print(h))
	wid.resize(500,300)
	sys.exit(app.exec_())
	
```

