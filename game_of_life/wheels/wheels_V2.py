import pygame

import math
from myWheel import *
from gui2oneUI import *

pygame.init()
pygame.key.set_repeat(300,50)

screen = pygame.display.set_mode((600, 500))
def callbackFunction1():
        print "callBack Function 1 !!!!!!!!!!!"
        
def callbackFunction2():
        print "callBack Function 2 !!!!!!!!!!!"
        
ui = gui2oneUI(screen)
##btn1 = Button(screen,20,20,100,20,"+ scale")
##btn1.draggable = True
##btn1.setCallback(callbackFunction1.func_code)
##
##
##ui.addItem(btn1)
##
##btn2 = Button(screen,20,60,100,20,"+ ssqd")
##btn2.draggable = True
##btn2.setCallback(callbackFunction2.func_code)
##ui.addItem(btn2)
##btn3 = Button(screen,20,100,100,20)    
##ui.addItem(btn3)


uiY = 10
uiY += 50
slider1 = Slider(screen, 20, uiY, 100 ,30, "Time Scale",0.3)
ui.addItem(slider1)
    

uiY += 50
slider2 = Slider(screen, 20, uiY, 100 ,30, "Radius Mult",1.0)
ui.addItem(slider2)

uiY += 50
slider_W2_radialOffset = Slider(screen, 20, uiY, 100 ,30, "W2 Radial Offset",0.2)
ui.addItem(slider_W2_radialOffset)

uiY += 50
slider_W2_radius = Slider(screen, 20, uiY, 100 ,30, "W2 radius",0.2)
ui.addItem(slider_W2_radius)


uiY += 100
slider_W3_radialOffset = Slider(screen, 20, uiY, 100 ,30, "W3 Radial Offset",0.96)
ui.addItem(slider_W3_radialOffset)

uiY += 50
slider_W3_radius= Slider(screen, 20, uiY, 100 ,30, "W3 radius",0.3)
ui.addItem(slider_W3_radius)


uiY += 50
text1 = StaticText(screen, 20, uiY, 100 ,30)
ui.addItem(text1)






done = False
is_blue = True
posx = screen.get_width()/2.0
time = 0.0
clock = pygame.time.Clock()

paused = False
SPEED = 1.0
speedMult = 1.0;
RADIUS_MULT = 1.0

##btn1 = Button(screen,20,20,"+ scale")
##btn2 = Button(screen,20,55,"- scale")    
while not done:

    speedMult = slider1.value*10.0
    RADIUS_MULT = slider2.value
    if RADIUS_MULT == 0: 
        RADIUS_MULT = 0.01
    time += clock.get_time()*0.0005 * SPEED * speedMult

    offsetx = (math.cos(time)*200.0) + posx
    screen.fill((0, 0, 0))
    

    ui.eventUpdate()
    ui.draw()     

    w1 = myWheel(screen)
    w1.setPosition(350,200)
    w1.radius = 100.0 * RADIUS_MULT
    w1.setRotation(offsetx)
    w1.draw()

    w2 = myWheel(screen)
    #w2.setPosition(offsetx,200)
    w2.radialOffset = slider_W2_radialOffset.value
    W2_RADIUS = slider_W2_radius.value * 200.0
    if W2_RADIUS == 0: 
        W2_RADIUS = 0.01
    w2.radius = W2_RADIUS * RADIUS_MULT
    w2.setParent(w1)
    w2.setRotation(offsetx)
    w2.draw()

    
    w3 = myWheel(screen)
    w3.radialOffset = slider_W3_radialOffset.value
    W3_RADIUS = slider_W3_radius.value * 200.0
    if W3_RADIUS == 0: 
        W3_RADIUS = 0.01
    w3.radius = W3_RADIUS * RADIUS_MULT                
    w3.setParent(w2)
    w3.setRotation(offsetx)
    w3.draw()        

    text1.text = str(w2.rotation / (math.pi*2.0))
    
           
        
    pygame.display.flip()
    # will block execution until 1/60 seconds have passed 
    # since the previous time clock.tick was called. 
    clock.tick(60)        


##pygame.quit()
