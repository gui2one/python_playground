from PySide import QtCore, QtGui, QtOpenGL
import sys



from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class myApp(QtGui.QWidget):
    def __init__(self):
        super(myApp, self).__init__()
        self.setupUI()
        pass
    def setupUI(self):
        myGL = MyGLDrawer()
        myGL.initializeGL()


class MyGLDrawer(QtOpenGL.QGLWidget):

    def __init__(self):
        QtOpenGL.QGLWidget.__init__(self)
        # print "valid", QtOpenGL.QGLWidget.isValid(self)
        # glutInit()
        # pass

    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho( -.5, .5, .5, -.5, -1000, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClearColor(1.0, 1.0, 1.0, 1.0)


    def resizeGL(self, w, h):
        # setup viewport, projection etc.:
        glViewport(0, 0, w, h)



    def paintGL(self):
        # draw the scene:

        # glRotatef(...)
        # glMaterialfv(...)
        # QtOpenGL.glBegin(GL_QUADS)
        # QtOpenGL.glVertex3f(0,1,0)
        # QtOpenGL.glVertex3f(1,0,0)

        # QtOpenGL.glEnd()
        pass


if __name__ == "__main__":
    print "not main"
    app = QtGui.QApplication(sys.argv)
    myWindow = myApp()

    print myWindow
    myWindow.show()
    sys.exit(app.exec_())