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
		self.open_button = self.add_open_button()
		self.datalayout.addWidget(self.open_button)
		self.setLayout(self.datalayout)
		self.show()
		self.tree = QTreeWidget()
		header = QTreeWidgetItem(['File','Type','H5 Keys'])
		self.tree.setHeaderItem(header)
		self.datalayout.addWidget(self.tree)
	
	def add_open_button(self):
		open_file_btn = QPushButton('Open')
		open_file_btn.clicked.connect(self.add_file)
		#button_section =  QHBoxLayout()
		#button_section.addWidget(open_file_btn)
		return open_file_btn#button_section
		
	def add_file(self):	
		h5file = QFileDialog.getOpenFileName(self, 'Open file',
		'/home/yugang/Desktop/XPCS_GUI/TestData/test.h5', filter='*.hdf5 *.h5 *.lst')[0]
		self.f = h5py.File(h5file,'r')
		self.filename = self.f.filename.split('/')[-1]
		
		#self.model = QStandardItemModel(0,3)
		#self.model.setHeaderData(0,Qt.Horizontal,"File")
		#self.model.setHeaderData(1,Qt.Horizontal,"Type")
		#self.model.setHeaderData(2,Qt.Horizontal,"H5 keys")
		
		
		self.tree_root = QTreeWidgetItem(self.tree,[self.filename,'H5 File',''])
		self.tree.setColumnWidth(0,250)
		self.tree.setColumnWidth(1,100)
		self.tree.setColumnWidth(2,100)
		print(
			  self.tree.columnWidth(0),
			  self.tree.columnWidth(1),
			  self.tree.columnWidth(2))
		self.add_branch(self.tree_root,self.f)
		#self.tree.setModel(self.model)
		self.tree.itemClicked.connect(self.onItemClicked)
		
		#print(self.tree.currentItem())
		self.setLayout(self.datalayout)
		self.show()

	def add_branch(self,tree_root,h5file):
		for _ in h5file.keys():
			#print(self.tree.currentItem())
			branch = QTreeWidgetItem([str(h5file[_].name).split('/')[-1],
									  str(type(h5file[_])),
									  str(h5file[_].name)])
			tree_root.addChild(branch)
			if 	isinstance(h5file[_],h5py.Group):
				self.add_branch(branch,h5file[_])
	
	@pyqtSlot(QTreeWidgetItem,int)
	def onItemClicked(self,item):
		print(self.filename,item.text(2))
	#def add_data(self,parent_model,h5file):
	#	for _ in h5file.keys():
	#		parent_model.insertRow(0)# = QStandardItemModel(0,3)
	#		parent_model.setData(parent_model.index(0,0),self.filename)
	#		parent_model.setData(parent_model.index(0,1),str(type(h5file)))
	#		parent_model.setData(parent_model.index(0,2),str(h5file[_].name))
	#		#model.appendRow(model)
	#		if 	isinstance(h5file[_],h5py.Group):
	#			self.add_data(parent_model,h5file[_])
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	Tree = tree()
	sys.exit(app.exec_())
