
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math


#-----------
# VARIABLES
#-----------

g_fViewDistance = 9.
g_Width = 600
g_Height = 600

g_nearPlane = 1.
g_farPlane = 1000.

action = ""
xStart = yStart = 0.
zoom = 65.

xRotate = 0.
yRotate = 0.
zRotate = 0.

xTrans = 0.
yTrans = 0.


deltaX= 0.
deltaY = 0.

oldMouseX = 0.
oldMouseY = 0.



phi = 0.0
theta = 0.0
radius =  10.0

camPosX = 0.
camPosY = 0.
camPosZ = -radius

radiusInc = radius

angleX = 0.
angleY = 0.
angleZ = 0.

justPressed = False
#-------------------
# SCENE CONSTRUCTOR
#-------------------


def readFile(filePath):

    f = open(filePath, 'r')
    data = f.read()
    f.close()
    return data


def createShader():

    vertCode = readFile('shaders/vertex_shader.vert')
    VERTEX_SHADER = shaders.compileShader(vertCode, GL_VERTEX_SHADER)

    fragCode = readFile('shaders/fragment_shader.frag')
    FRAGMENT_SHADER = shaders.compileShader(fragCode, GL_FRAGMENT_SHADER)    

    shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)

    return shader


def scenemodel(shader):
    # glRotate(90,0.,0.,1.)
    shaders.glUseProgram(shader)
    myUniformLocation = glGetUniformLocation(shader, "myUniform");
    glUniform4f(myUniformLocation, 0.2,0.5,1.0,1.0);
    glutSolidTeapot(1.)
    glDeleteProgram(shader)

def cubeModel(shader):
    glTranslate(3.0,0.,0.)
    shaders.glUseProgram(shader)
    myUniformLocation = glGetUniformLocation(shader, "myUniform");
    glUniform4f(myUniformLocation, 0.9,0.3,0.3,1.0);    
    glutSolidCube(1.)  
    glDeleteProgram(shader)  


#--------
# VIEWER
#--------

def printHelp(): 
    print """\n\n    
         -------------------------------------------------------------------\n
         Left Mousebutton       - move eye position (+ Shift for third axis)\n
         Middle Mousebutton     - translate the scene\n
         Right Mousebutton      - move up / down to zoom in / out\n
          Key r               - reset viewpoint\n
          Key q               - exit the program\n
         -------------------------------------------------------------------\n
         \n"""


def init():
    # glEnable(GL_NORMALIZE)
    glLightfv(GL_LIGHT0,GL_POSITION,[ .0, 10.0, 10., 0. ] )
    glLightfv(GL_LIGHT0,GL_AMBIENT,[ .0, .0, .0, 1.0 ]);
    glLightfv(GL_LIGHT0,GL_DIFFUSE,[ 1.0, 1.0, 1.0, 1.0 ]);
    glLightfv(GL_LIGHT0,GL_SPECULAR,[ 1.0, 1.0, 1.0, 1.0 ]);
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    resetView()


def resetView():
    global zoom, xRotate, yRotate, zRotate, xTrans, yTrans
    zoom = 65.
    xRotate = 0.
    yRotate = 0.
    zRotate = 0.
    xTrans = 0.
    yTrans = 0.
    glutPostRedisplay()


def display():
    # Clear frame buffer and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glClearColor(0.,0.,0.,1.)
    # Set up viewing transformation, looking down -Z axis
    glLoadIdentity()

    # Set perspective (also zoom)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #gluPerspective(zoom, float(g_Width)/float(g_Height), g_nearPlane, g_farPlane)
    glOrtho(0.0,10.0,0.0,1.0,0.0,1000.0)
    glMatrixMode(GL_MODELVIEW)
    # Render the scene
    gluLookAt(camPosX , camPosY, camPosZ, 0., 0., 0.,0,1,0)   #-.1,0,0
    moveCamera()
    # glColor3f(1.,0.,0.)
    shader = createShader()
    scenemodel(shader)
    
    # glColor3f(1.,1.,0.)
    cubeModel(shader)
    
    # Make sure changes appear onscreen
    glutSwapBuffers()


def reshape(width, height):
    global g_Width, g_Height
    g_Width = width
    g_Height = height
    glViewport(0, 0, g_Width, g_Height)
    
def moveCamera():

    global deltaX, deltaY, oldMouseX, oldMouseY, camPosX, camPosY, camPosZ
    global radius, phi, theta



    if action == 'left' :
        theta += deltaX
        angleLimit = 85

        if phi >= angleLimit:
            phi = angleLimit-0.01
        elif phi <= -angleLimit:
            phi = -angleLimit+0.01
        if phi+deltaY <= angleLimit and phi+deltaY >= -angleLimit:
            phi += deltaY 
        # print 'theta -->' ,theta, 'phi -->', phi   , 'radius -->', radius
    elif action == 'zoom_pos' :   
        radius = radiusInc
        
        
    elif action == 'zoom_neg' :
        radius = radiusInc
        

    camPosX = math.sin(math.radians(theta))* math.cos(math.radians(phi))*radius
    camPosY = math.sin(math.radians(phi))*radius
    camPosZ = math.cos(math.radians(theta))* math.cos(math.radians(phi))* -radius


   

def keyboard(key, x, y):
    global zTr, yTr, xTr
    if(key=='r'): resetView()
    if(key=='q'): exit(0)
    glutPostRedisplay()


def mouse(button, state, x, y):
    global action, xStart, yStart, justPressed
    global radiusInc, radius
    if (button==GLUT_LEFT_BUTTON):
        if (glutGetModifiers() == GLUT_ACTIVE_SHIFT):
            action = "MOVE_EYE_2"
            
        else:
            action = "left"
            print 'state : ',state, justPressed
            if state == 0 : # pressed
                justPressed = True
    elif (button==GLUT_MIDDLE_BUTTON):
        action = "wheel"
    elif (button==GLUT_RIGHT_BUTTON):
        action = "ZOOM"


    elif button == 3 and state == GLUT_UP:
        action = 'zoom_pos'            
        radiusInc -= 1.
        print ' ZOOM IN ', 'radiusInc -->', radiusInc, radius

        

    elif button == 4 and state == GLUT_UP:
        action = 'zoom_neg'            
        radiusInc += 1.

        print ' ZOOM OUT'

    xStart = x
    yStart = y


def motion(x, y):
    # global zoom, xStart, yStart, xRotate, yRotate, zRotate, xTrans, yTrans
    global oldMouseX, oldMouseY, deltaX, deltaY
    global action, justPressed, radius,radiusInc

    if not justPressed and action=='left':
        deltaX = x - oldMouseX
        deltaY = y - oldMouseY 
    if justPressed and action=='left':
        justPressed = False
        print 'just PRESSED'
        deltaX = 0
        deltaY = 0
    if action == 'zoom_pos' or action == 'zoom_neg':
        radius = radiusInc
        print radius
    if action == 'wheel' :
        print 'WHEEL !!!!!!!!!!!!!!!'
    # xStart = x
    # yStart = y 


    oldMouseX = x
    oldMouseY = y
    glutPostRedisplay()


#------
# MAIN
#------
if __name__=="__main__":
    # GLUT Window Initialization
    glutInit()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB| GLUT_DEPTH)      # zBuffer
    glutInitWindowSize (g_Width,g_Height) 
    glutInitWindowPosition (0 + 4, g_Height / 4)
    glutCreateWindow ("Visualizzatore_2.0")
    # Initialize OpenGL graphics state
    init ()
    # Register callbacks
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)    
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    printHelp()
    # Turn the flow of control over to GLUT
    glutMainLoop()