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
        
             
      
      srcPath = "f:/HOUDINI_CONFIG/OTLs/"
      dstPath = "C:\Users\CORSAIR\Documents\western\Assets\OTLs"


      QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
      
      self.setToolTip('This is a <b>QWidget</b> widget -- self')
      
      

      listSrc = QtGui.QListView(self)
      listSrc.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
      listSrc.resize(300,300)
      listSrc.move(10,40)

      self.initList(listSrc, srcPath)


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

      self.initList(listDst, dstPath)

      #print(dir(listDst))
      btnDst = QtGui.QPushButton('Browse Destination Directory', self)
      btnDst.setToolTip('This is a <b>QPushButton</b> widget')
      btnDst.resize(btnDst.sizeHint())
      btnDst.move(350, 10)       
      btnDst.clicked.connect(lambda: self.feedList(listDst))      



      btnCopy = QtGui.QPushButton('>>', self)
      btnCopy.move(310, 150)   
      btnCopy.setFixedWidth(30)
      btnCopy.setFixedHeight(50)
      btnCopy.clicked.connect(lambda: self.copyHDAs())




      self.setGeometry(300, 300, 700, 350)
      self.setWindowTitle('HDA Manager')    
      self.show()

    def copyHDAs(self):
      global dstPath
      print dstPath


    def initList(self,list,path) :
      

      os.chdir(path) # sets the working directory
      fileNames = glob("*")  
      print fileNames           

      model = QtGui.QStandardItemModel(list)
      for afile in fileNames :
       
        if os.path.isfile(afile) :
            if afile.endswith("otl") | afile.endswith("hdalc") :
              item = QtGui.QStandardItem(afile)
              item.setCheckable(True)
              item.setToolTip('HDA file')
              model.appendRow(item)

      list.setModel(model)


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
              item.setToolTip('self')

              model.appendRow(item)

      list.setModel(model)

      



        
def main():
    
  app = QtGui.QApplication(sys.argv)
  ex = Example()
  sys.exit(app.exec_())


if __name__ == '__main__':
  main()