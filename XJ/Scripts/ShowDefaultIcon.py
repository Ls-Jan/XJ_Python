
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

'''
	展示Qt的自带图标
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w=QWidget()
    table=QGridLayout(w)

    for i in range(100):
        btn=QPushButton()
        btn.setStyleSheet('font-size:20px;background:transparent')
        table.addWidget(btn,int(i/10),i%10)
        btn.setIcon(QApplication.style().standardIcon(i))
        btn.setToolTip(str(i))

    w.show()
    w.resize(1500,400)
    # te=QTextEdit()
    # te.show();
    # te.setHtml("图片：<img src='./Test.jpg'><br>");
    sys.exit(app.exec())


