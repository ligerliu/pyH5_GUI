import sys
from PyQt5.QtWidgets import (QPushButton, QHBoxLayout, QApplication, QWidget, QTreeView, QTreeWidget, QVBoxLayout, QTreeWidgetItem,QFileDialog)
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot,QSize
import h5py
from py4xs.hdf import lsh5

class tree(QWidget):
	(FILE,FILE_PATH,H5GROUP) = range(3)
	def __init__(self):
		super().__init__()
		self.title = 'Tree of h5 data'
		self.left = 10
		self.top = 10
		self.width = 720
		self.height = 640
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		
		self.datalayout= QVBoxLayout()
		self.tree = QTreeWidget()
		header = QTreeWidgetItem(['File'])
		self.tree.setHeaderItem(header)
		self.datalayout.addWidget(self.tree)
	
	def add_file(self,h5file):	
		self.h5_file_path = h5file
		self.f = h5py.File(h5file,'r')
		self.filename = self.f.filename.split('/')[-1]
		
		self.tree_root = QTreeWidgetItem(self.tree,[self.filename,self.h5_file_path,''])
		self.tree.setColumnWidth(0,250)
		self.tree.setColumnWidth(1,0)
		self.tree.setColumnWidth(2,0)
		
		self.add_branch(self.tree_root,self.f)
		#self.tree.itemClicked.connect(self.onItemClicked)
		#self.setLayout(self.datalayout)
		#self.show()

	def add_branch(self,tree_root,h5file):
		for _ in h5file.keys():
			branch = QTreeWidgetItem([str(h5file[_].name).split('/')[-1],
									  str(self.h5_file_path),
									  str(h5file[_].name)])
			tree_root.addChild(branch)
			if 	isinstance(h5file[_],h5py.Group):
				self.add_branch(branch,h5file[_])
	
	@pyqtSlot(QTreeWidgetItem,int)
	def onItemClicked(self,item):
		print(self.filename,item.text(2))

class titledTable():
	def __init__(self,title):
		self.title = QLabel(title)
		self.table = QTableWidget()
		self.table.setShowGrid(True)
		
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.table)
		
	def clear():
		self.table.setRowCount(0)
		self.table.setColumnCount(0)
		self.clear()
	
	def set_item(self,row,col,item):
		if isinstance(item, str):
			self.table.setItem(row, col, QTableWidgetItem(item))
		else:
			print("Type Error: Item Must Be a String")
	
	def num_cols(self,values):
		value_shape = np.shape(values)
		numcols = 1
		
		if len(value_shape) > 1:	
			numcols = value_shape[1]	
		
#if __name__ == '__main__':
#	app = QApplication(sys.argv)
#	Tree = tree()
#	sys.exit(app.exec_())
