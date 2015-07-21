#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
from glob import glob
from PySide import QtGui

class Example(QtGui.QWidget):
    
    def __init__(self):
      super(Example, self).__init__()
      
      self.initUI()
        
    def initUI(self):
        
             


      QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
      
      self.setToolTip('This is a <b>QWidget</b> widget')
      
      

      listSrc = QtGui.QListView(self)
      listSrc.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
      listSrc.resize(300,300)
      listSrc.move(10,40)
      #print(dir(listSrc))
      btnSrc = QtGui.QPushButton('Browse Source Directory', self)
      btnSrc.setToolTip('This is a <b>QPushButton</b> widget')
      btnSrc.resize(btnSrc.sizeHint())
      btnSrc.move(10, 10)       
      btnSrc.clicked.connect(lambda: self.feedList(listSrc))


      listDst = QtGui.QListView(self)
      listDst.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
      listDst.resize(300,300)
      listDst.move(350,40)
      #print(dir(listDst))
      btnDst = QtGui.QPushButton('Browse Destination Directory', self)
      btnDst.setToolTip('This is a <b>QPushButton</b> widget')
      btnDst.resize(btnDst.sizeHint())
      btnDst.move(350, 10)       
      btnDst.clicked.connect(lambda: self.feedList(listDst))      



      self.setGeometry(300, 300, 700, 350)
      self.setWindowTitle('Tooltips')    
      self.show()


    def btnClicked(self) :
      print "button clicked !"


    def feedList(self, list) :
      print "browse function"
      dialog = QtGui.QFileDialog(self)
      dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
      dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)   
      if dialog.exec_() :

        srcFolderPath = dialog.selectedFiles()
        os.chdir(srcFolderPath[0]) # sets the working directory
        fileNames = glob("*")  
        print fileNames           
      model = QtGui.QStandardItemModel(list)
      for afile in fileNames :
        print str(afile.endswith("hdalc"))
        if os.path.isfile(afile) :
            if afile.endswith("otl") | afile.endswith("hdalc") :
              item = QtGui.QStandardItem(afile)
              item.setCheckable(True)

              model.appendRow(item)

      list.setModel(model)

      



        
def main():
    
  app = QtGui.QApplication(sys.argv)
  ex = Example()
  sys.exit(app.exec_())


if __name__ == '__main__':
  main()