#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
import shutil
from glob import glob
from PySide import QtGui



SRCPATH = "F:/HOUDINI_CONFIG/OTLs"
DSTPATH = "F:/TEMP"

class HDAManager(QtGui.QWidget):
    
    def __init__(self):
      super(HDAManager, self).__init__()
      
      self.initUI()
        
    def initUI(self):

      global SRCPATH
      global DSTPATH

      QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
      
      self.setToolTip('This is a <b>QWidget</b> widget -- self')
      
      

      self.listSrc = QtGui.QListView(self)
      self.listSrc.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
      self.listSrc.resize(300,300)
      self.listSrc.move(10,60)

      self.initList(self.listSrc, SRCPATH)


      #print(dir(listSrc))
      btnSrc = QtGui.QPushButton('Browse Source Directory', self)
      btnSrc.setToolTip('This is a <b>QPushButton</b> widget')
      btnSrc.resize(btnSrc.sizeHint())
      btnSrc.move(10, 10)       
      btnSrc.clicked.connect(lambda: self.feedSrcList())

      self.labelSrc = QtGui.QLabel(self)
      self.labelSrc.setText(SRCPATH)
      self.labelSrc.resize(300,30)
      self.labelSrc.move(10,40)


      self.labelDst = QtGui.QLabel(self)
      self.labelDst.setText(DSTPATH)
      self.labelDst.resize(300,30)
      self.labelDst.move(350,40)


      self.listDst = QtGui.QListView(self)
      self.listDst.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
      self.listDst.resize(300,300)
      self.listDst.move(350,60)

      self.initList(self.listDst, DSTPATH)

      #print(dir(listDst))
      self.btnDst = QtGui.QPushButton('Browse Destination Directory', self)
      self.btnDst.setToolTip('This is a <b>QPushButton</b> widget')
      self.btnDst.resize(self.btnDst.sizeHint())
      self.btnDst.move(350, 10)       
      self.btnDst.clicked.connect(lambda: self.feedDstList())      



      self.btnCopy = QtGui.QPushButton('>>', self)
      self.btnCopy.move(310, 150)   
      self.btnCopy.setFixedWidth(30)
      self.btnCopy.setFixedHeight(50)
      self.btnCopy.clicked.connect(lambda: self.copyHDAs(SRCPATH, DSTPATH))


      # self.resized.connect(lambda: seft.resizeWindow())

      self.setGeometry(300, 300, 680, 380)
      self.setWindowTitle('HDA Manager')    
      self.show()

    def copyHDAs(self,srcPath, dstPath):
      global SRCPATH
      global DSTPATH
      # for item in dir(self.listSrc):
      #   print item

      print self.listSrc.model().rowCount()
      selected = self.listSrc.selectedIndexes()

      for item in selected :
        print item.data(), "------->", DSTPATH
        # for meth in dir(item):
        #   print meth
        hdaName =  item.data()
        srcFilePath = str(SRCPATH)+"/"+hdaName
        dstFilePath = str(DSTPATH)+"/"+hdaName
        shutil.copyfile(srcFilePath,dstFilePath)
        

      self.initList(self.listDst,DSTPATH)

    def initList(self,list,path) :
      

      try: 
        os.chdir(path) # sets the working directory
        fileNames = glob("*")  
        # print fileNames          

        model = QtGui.QStandardItemModel(list)

        for afile in fileNames :         
          if os.path.isfile(afile) :
              if afile.endswith("otl") | afile.endswith("hdalc") :
                item = QtGui.QStandardItem(afile)
                # item.setCheckable(True)
                item.setToolTip('HDA file')
                model.appendRow(item)
        list.setModel(model)

      except:
        print "bad path"                




    def feedSrcList(self) :

      global SRCPATH

    

      # print listSrc
      # print "browse function"
      dialog = QtGui.QFileDialog(self)
      dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
      dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)   
      if dialog.exec_() :
        SRCPATH = dialog.selectedFiles()[0]
        srcFolderPath = SRCPATH

        self.labelSrc.setText(SRCPATH)

        os.chdir(srcFolderPath) # sets the working directory
        fileNames = glob("*")  
        # print fileNames           
      model = QtGui.QStandardItemModel(self.listSrc)
      for afile in fileNames :
        # print str(afile.endswith("hdalc"))
        if os.path.isfile(afile) :
            if afile.endswith("otl") | afile.endswith("hdalc") :
              item = QtGui.QStandardItem(afile)
              # item.setCheckable(True)
              item.setToolTip('self')

              model.appendRow(item)

      self.listSrc.setModel(model)

 
    def feedDstList(self) :
      global DSTPATH

    

      # print listSrc
      print "browse function"
      dialog = QtGui.QFileDialog(self)
      dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
      dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)   
      if dialog.exec_() :
        DSTPATH = dialog.selectedFiles()[0]
        dstFolderPath = DSTPATH

        self.labelDst.setText(DSTPATH)

        os.chdir(dstFolderPath) # sets the working directory
        fileNames = glob("*")  
        # print fileNames           
      model = QtGui.QStandardItemModel(self.listDst)
      for afile in fileNames :
        print str(afile.endswith("hdalc"))
        if os.path.isfile(afile) :
            if afile.endswith("otl") | afile.endswith("hdalc") :
              item = QtGui.QStandardItem(afile)
              # item.setCheckable(True)
              item.setToolTip('self')

              model.appendRow(item)

      self.listDst.setModel(model)     


     
    def resizeEvent(self,event):
      # print 'resizing ....', event.size().width(), event.size().height()
      width1 = (event.size().width()*0.5) - 40.0
      height1 = event.size().height()-70.0
      self.listSrc.resize(width1, height1)
      self.btnCopy.move(width1+10.0, event.size().height()/2)
      self.listDst.resize(width1, height1)
      self.listDst.move(width1+ 40.0, 60.0)

      self.labelDst.move(width1+ 40.0,40)

      self.btnDst.move(width1 + 40.0,10.0 )




def main():
    
  app = QtGui.QApplication(sys.argv)
  ex = HDAManager()
  sys.exit(app.exec_())


if __name__ == '__main__':
  main()

