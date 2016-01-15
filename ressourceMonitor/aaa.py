import sys

# Import Qt modules
from PySide import QtCore,QtGui, QtOpenGL, QtUiTools
class ressourceMonitor(QtGui.QWidget):
    
    def __init__(self):
      super(ressourceMonitor, self).__init__()
      
      self.initUI()
        
    def initUI(self):
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile("ressourceMonitorUI/mainwindow.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.myWidget = loader.load(file)
        file.close()

        self.myWidget.show()

        print self.myWidget.graphicsView
        self.drawThings()



    def drawThings(self):

        print self.myWidget.graphicsView
        pass

        # self.show()


def main():
    
  app = QtGui.QApplication(sys.argv)
  ex = ressourceMonitor()
  sys.exit(app.exec_())


if __name__ == '__main__':
  main()