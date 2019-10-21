import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QTreeWidget, QVBoxLayout, QTreeWidgetItem
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot,QSize
import h5py
from py4xs.hdf import lsh5

class tree(QWidget):
	(FILE,FILE_PATH,H5GROUP) = range(3)
	def __init__(self,h5file=None):
		super().__init__()
		self.title = 'Tree of h5 data'
		self.left = 10
		self.top = 10
		self.width = 720
		self.height = 640
		self.f = h5py.File(h5file,'r')
		self.filename = self.f.filename.split('/')[-1]
		self.UI()
	
	def UI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		
		datalayout= QVBoxLayout()
		self.tree = QTreeWidget()
		header = QTreeWidgetItem(['File','Type','H5 Keys'])
		self.tree.setHeaderItem(header)
		datalayout.addWidget(self.tree)
		
		#self.model = QStandardItemModel(0,3)
		#self.model.setHeaderData(0,Qt.Horizontal,"File")
		#self.model.setHeaderData(1,Qt.Horizontal,"Type")
		#self.model.setHeaderData(2,Qt.Horizontal,"H5 keys")
		
		
		self.tree_root = QTreeWidgetItem(self.tree,[self.filename,'H5 File',''])
		self.tree.setColumnWidth(0,250)
		print(
			  self.tree.columnWidth(0),
			  self.tree.columnWidth(1),
			  self.tree.columnWidth(2))
		self.add_branch(self.tree_root,self.f)
		#self.tree.setModel(self.model)
		self.tree.itemClicked.connect(self.onItemClicked)
		
		#print(self.tree.currentItem())
		self.setLayout(datalayout)
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
	Tree = tree(h5file='/Users/jiliangliu/Downloads/U_minn_batch5.h5')
	sys.exit(app.exec_())
