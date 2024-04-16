
from XJ.ModuleTest.XJQ_PackageTest import XJQ_PackageTest
from PyQt5.QtWidgets import QApplication


if __name__=='__main__':
	packages={package:f'./XJ/{package}' for package in ['Widgets','Functions','Structs']}
	app=QApplication([])
	pt=XJQ_PackageTest(**packages)
	pt.show()
	exit(app.exec())



