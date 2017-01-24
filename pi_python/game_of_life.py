## game of life

import pygame
import math
import random
from threading import Thread
import sys
sys.path.insert(0,"./wheels")
from gui2oneUI import *


class GOL_grid(object):
    def __init__(self, position = [20,20], size=[30,30]):

        self.size = size
        self.position = position
        self.cells = []
        self.cellSize = 8
        
        self.font = pygame.font.Font(pygame.font.get_default_font(),10)

        self.showCellNums = False
        self.iterations = 0
        self.isEvolving = True

        self.startString = ''
    
    def build(self):
        counter = 0
        for j in range(0,self.size[1]):

            for i in range(0,self.size[0]):
                
                boolTest = int(random.random() < 0.5)
                self.startString += str(boolTest)
                
                cell = GOL_cell(boolTest)
 
                cell.coords = [i,j]
                self.cells.append(cell)

                counter += 1        

        #print random.random()

    def buildByString(self, _string):
        self.iterations = 0
        self.isEvolving = True        
        counter = 0
        self.startString = _string
        self.cells = []
        for j in range(0,self.size[1]):

            for i in range(0,self.size[0]):
                
                
                
                boolTest = int(self.startString[i+(j*self.size[0])])
                cell = GOL_cell(boolTest)
 
                cell.coords = [i,j]
                self.cells.append(cell)

                counter += 1          
    def getNumNeighbours(self,cell):
        x = cell.coords[0]
        y = cell.coords[1]
        width = self.size[0]
        height = self.size[1]
        
        curID = (y * width) + x

        ids = []
        ## starting from top left corner , clockwise
        if x > 0 and y > 0 :        ### id 0
            ids.append(curID - width - 1)
        if y > 0 :                  ### id 1
            ids.append(curID - width)
        if x < width-1 and y > 0:   ### id 2
            ids.append(curID - width + 1)
        if x < width-1:             ### id 3
            ids.append(curID + 1)
        if x < width-1 and y < height-1:### id 4
            ids.append(curID + width + 1)
        if y < height-1:            ### id 5
            ids.append(curID + width)
        if x > 0 and y < height-1:  ### id 6
            ids.append(curID + width - 1)
        if x > 0:                   ### id 7
            ids.append(curID - 1)

        cell.numBuddies = 0
        for i in range(0,len(ids)):
            if(self.cells[ids[i]].state == 1):
                cell.numBuddies += 1

                
        return cell.numBuddies


    def checkBuddies(self):
        for i in range(0,len(self.cells)):

            cell = self.cells[i]
            #if i == 6 : print  self.getNumNeighbours(cell)
            numBuddies = self.getNumNeighbours(cell)

            self.cells[i].numBuddies = numBuddies
    def getString(self):
        gridString = ''
        for cell in self.cells : gridString += str(cell.state)

        return gridString
            
    def update(self):

        if self.isEvolving:
            self.checkBuddies()
            for i in range(0,len(self.cells)):

                cell = self.cells[i]
                cell.temperature *= 0.3
                if cell.state == 1:
                    cell.temperature = 1.0
                    if cell.numBuddies < 2 or cell.numBuddies > 3:
                        cell.state = 0
                    elif cell.numBuddies == 2 or cell.numBuddies == 3:
                        pass
                else:
                    if cell.numBuddies == 3:
                        cell.state = 1
                        cell.temperature = 1.0

                
                
            self.iterations += 1
            
    
    def draw(self):
        #print "draw!!!!"
        
        
        for i in range(0,len(self.cells)):
            cell = self.cells[i]
       
            temp = int(cell.temperature*255)
            clr = (temp, temp, temp)
            pygame.draw.rect(screen, clr,pygame.Rect((cell.coords[0]*self.cellSize)+ self.position[0],(cell.coords[1]*self.cellSize)+ self.position[1],self.cellSize-2,self.cellSize-2))

            if self.showCellNums:
                textSurface = self.font.render(str(i), True, (255,255,255))
                
                textPosX = cell.coords[0]* self.cellSize
                textPosY = cell.coords[1]* self.cellSize        
                screen.blit(textSurface,(textPosX,textPosY))

                textSurface = self.font.render(str(cell.numBuddies), True, (100,255,100))
                
                textPosX = (cell.coords[0]* self.cellSize)+ 10
                textPosY = (cell.coords[1]* self.cellSize)+ 10
                screen.blit(textSurface,(textPosX,textPosY))

                textSurface = self.font.render(str(cell.coords), True, (255,255,200))
                
                textPosX = (cell.coords[0]* self.cellSize)+ 10
                textPosY = (cell.coords[1]* self.cellSize)+ 25
                screen.blit(textSurface,(textPosX,textPosY))                  
        
class GOL_cell(object):
    def __init__(self, state=1, coords=[0,0]):
        self.state = state
        self.coords = coords
        self.numBuddies = 0
        self.temperature = 0




pygame.init()
screen = pygame.display.set_mode((700, 700))




isEvolving = True




pygame.display.set_caption("Game Of Life")
ui = gui2oneUI(screen)

iterText = StaticText(screen,220,30,200,50)
iterText.setFontSize(13)
ui.addItem(iterText)

recordText = StaticText(screen,220,60,200,50)
recordText.setFontSize(13)
ui.addItem(recordText)

resetBtn = Button(screen, 10,10,60,20, "Reset")
resetBtn.setFontSize(13)
record = 0
frameCounter = 0

gridSize = 25
gridPos = [50,100]  
grid = GOL_grid(gridPos,[gridSize,gridSize])

def buildGrid():

    #global grid
    grid.__init__(gridPos,[gridSize,gridSize])
    grid.cellSize = 10
    grid.build()      
    oldGridString = ''
    grid.isEvolving = True
    global frameCounter
    frameCounter = 0


resetBtn.subscribe(buildGrid)


ui.addItem(resetBtn)


pauseBtn =  Button(screen, 10,35,60,20, "Pause")
pauseBtn.setFontSize(13)

def pauseGrid():
    #print pauseBtn
    grid.isEvolving = not grid.isEvolving
    
pauseBtn.subscribe(pauseGrid)
ui.addItem(pauseBtn)


def playRecord():
    print recordString
    grid.buildByString(recordString)
    
playRecordBtn = Button(screen, 10,60,60,20, "Play Record")
playRecordBtn.fontSize = 10
playRecordBtn.subscribe(playRecord)
ui.addItem(playRecordBtn)

timeSlider = Slider(screen,80,60,150,30,"time",0.0)
ui.addItem(timeSlider)


buildGrid()
oldGridString = grid.getString()




clock = pygame.time.Clock()
done = False



recordString = ''
grid.draw()
while not done:
    screen.fill((0, 0, 0))
    ui.eventUpdate()
    ui.draw()
    
    if grid.iterations % 6 == 0  and grid.iterations > 2 :
        
        newString = grid.getString()
        
        if oldGridString == newString:
            grid.isEvolving = False            
            if grid.iterations > record :
                recordString = grid.startString
                record = grid.iterations - 6 ### subtract same as modulo up there
                
            buildGrid()

        else:            
            oldGridString = newString

    

    
    
    
    grid.update()   
    
        
    iterText.text = "Iterations : " +str(grid.iterations)
    recordText.text = "Record : "+ str(record)
    grid.draw()

    #print frameCounter
    frameCounter += 1
    

    
    clock.tick(30)

    pygame.display.flip()
    
    
