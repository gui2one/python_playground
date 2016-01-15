#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
# import os
# import shutil
# from glob import glob
from PySide import QtGui



SRCPATH = "F:/HOUDINI_CONFIG/OTLs"
DSTPATH = "F:/TEMP"

class ressourceMonitor(QtGui.QWidget):
    
    def __init__(self):
      super(ressourceMonitor, self).__init__()
      
      self.initUI()
        
    def initUI(self):

      global SRCPATH
      global DSTPATH

      QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
      

      
      scene = QtGui.QGraphicsScene(0,0,300,300)
      graph = QtGui.QGraphicsView(scene,self)

      brush = QtGui.QBrush(QtGui.QColor(255,10,20,255))
      

      # painter.setBrush(brush)
      # painter.drawEllipse(0, 0, 25, 25)
      # painter.setFont(Colors.tickerFont())
      # painter.setPen(QtGui.QColor(255, 255, 255, 255))
      # painter.drawText(10, 15, self.letter)

      #scene.drawRect(10,10,30,30)
      
      graph.setBackgroundBrush(brush)
      print graph.backgroundBrush()

      graph.show()
      graph.update()
      graph.setToolTip('This is a graphicsView -- self')
      # scene.show()
      self.setToolTip('This is a <b>QWidget</b> widget -- self')
      
      


      
      self.setGeometry(300, 300, 680, 380)
      self.setWindowTitle('Ressource Monitor')    
      self.show()
     
    # def resizeEvent(self,event):
    #   # print 'resizing ....', event.size().width(), event.size().height()





def main():
    
  app = QtGui.QApplication(sys.argv)
  ex = ressourceMonitor()
  sys.exit(app.exec_())


if __name__ == '__main__':
  main()

