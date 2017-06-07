import pygame
import math
import random

import serial


import sys
sys.path.insert(0,"./modules")
from gui2oneUI import *

pygame.init()
screen = pygame.display.set_mode((800, 700))

# pygame.display.set_caption("Game Of Life")
ui = gui2oneUI(screen)

slider1 = Slider(screen, 10,10,100,30,"time",0.0)
#slider1.setVisible = True
ui.addItem(slider1)

done = False

while not done:

    screen.fill((0, 0, 0))


    ui.eventUpdate()


    ui.draw()	

    pygame.display.flip()

pygame.quit()