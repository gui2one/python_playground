# Code Example: Display a window in PyQt4
# Python 2.6 with PyQt 4
import sys
from PyQt4 import QtGui
class MainFrame(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Oh la belle fenetre !!") # title
        self.resize(512, 100) # size
        self.setMinimumSize(512, 100) # minimum size
        self.move(0, 0) # position window frame at top left
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    frame = MainFrame()
    frame.show()
    
    exit_code = app.exec_()
    sys.exit(exit_code)