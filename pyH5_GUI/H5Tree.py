import numpy as np
import h5py

from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QMessageBox, QDesktopWidget,QMainWindow,
QAction, qApp, QMenu, QTreeWidget, QVBoxLayout, QLabel,
                QTableWidget, QTreeWidgetItem, QTableWidgetItem,
)
from PyQt5.QtGui import QFont ,  QIcon

from PyQt5 import QtCore, QtGui
#import PyQt5.QtWidgets as QtGui


class aboutWindow(QMessageBox):
    def __init__(self, parent=None):
        super(aboutWindow, self).__init__(parent)
        self.setWindowTitle('About XSH5View')
        self.setText('''
This is a working project for the development of GUI for the visulization of HDF files.
Some functions are dedicated to view XPCS results generated by pyCHX package developed at CHX beamline, NSLS-II, BNL.
Such functions include plot_g2, show_C12, etc.
Please contact Dr. Yugang Zhang at yuzhang@bnl.gov for more information.
I am not responsible for any issues that may arise from the use of this code, including any loss of data etc.
        ''')

class plotOptionWindow(QWidget):
    def __init__(self, parent=None):
        super(plotOptionWindow, self).__init__(parent)
        self.setWindowTitle('Plot Options')


class titledTree():
    def __init__(self, title):

        #self.list = QTreeWidget()

        self.tree = QTreeWidget()
        self.title = QLabel(title)
        #self.list.setHeaderLabel(str(title))
        self.tree.header().close()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.tree)

        self.grandpa_list = {}
        self.parent_list = {}# []
        self.child_list = {}

        self.group_list = []
        self.has_attrs_list = []


    def clear(self):
        self.row_list = {} # []
        self.group_list = []
        self.has_attrs_list = []
        self.tree.clear()

    def add_filename(self, sfilename, grandpa_name=None ):
        if grandpa_name is None:
            self.parent_list[sfilename] = QTreeWidgetItem(self.tree)
            self.parent_list[sfilename].setText(0,  sfilename )
            self.child_list[sfilename] = [ ]
        else:
            if grandpa_name not in list(self.grandpa_list.keys()):
                self.grandpa_list[grandpa_name] = QTreeWidgetItem(self.tree)
                self.grandpa_list[grandpa_name].setText(0,  grandpa_name )
            #print(  sfilename, grandpa_name, self.grandpa_list[grandpa_name] )    
            self.parent_list[sfilename] = QTreeWidgetItem(  self.grandpa_list[grandpa_name]   )
            self.parent_list[sfilename].setText(0,  sfilename )
            self.child_list[sfilename] = [ ]

    def add_item(self, parent_index, item, hdf5_file, sfilename ):

        parent = self.parent_list[sfilename]
        item_text = item.split('/')[-1]
        #self.row_list[-1].setText(0, item_text)
        is_group = isinstance(hdf5_file[item], h5py.Group)
        self.group_list.append(is_group)

        has_attrs = len(list(hdf5_file[item].attrs.keys())) > 0
        self.has_attrs_list.append(has_attrs)

        if parent_index == None:
            #Prt.append(QTreeWidgetItem(self.list))
            child = QTreeWidgetItem( parent )
            child.setText(0,  item_text )
            self.child_list[sfilename].append( child )
        else:
            self.child_list[sfilename].append( self.child_list[sfilename][-1] )
            self.child_list[sfilename][-1].setText(0,  item_text )


    def full_item_path(self, selected_row):
        text = selected_row.text(0)
        parent_row = selected_row.parent()

        while not parent_row == None:
            text = parent_row.text(0) + '/' + text
            parent_row = parent_row.parent()

        return text


    def swap_group_icon(self):
        for i in range(len(self.row_list)):
            if self.row_list[i].isExpanded():
                if self.has_attrs_list[i]:
                        self.row_list[i].setIcon(0, self.icon_open_group_with_attrs)
                else:
                    self.row_list[i].setIcon(0, self.icon_open_group)

            elif self.group_list[i] == True:
                if self.has_attrs_list[i]:
                    self.row_list[i].setIcon(0, self.icon_closed_group_with_attrs)
                else:
                    self.row_list[i].setIcon(0, self.icon_closed_group)
                #self.row_list[i].setIcon(0, self.closed_group_icon)


class titledTable():
    def __init__(self, title):
        self.title = QLabel(title)
        self.table = QTableWidget()
        self.table.setShowGrid(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.table)


    def clear(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.clear()


    def set_item(self, row, col, item):
        if isinstance(item, str):
            self.table.setItem(row, col,  QTableWidgetItem(item))
        else:
            print("Type Error: Item must be a str")


    def num_cols(self, values):
        value_shape = np.shape(values)
        numcols = 1

        if len(value_shape) > 1:
            numcols = value_shape[1]

        return numcols
