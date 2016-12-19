## game of life

import pygame
import math
import random

import sys
sys.path.insert(0,"./modules")
from gui2oneUI import *



class GOL_cell(object):
    def __init__(self, state=1, coords=[0,0]):
        self.state = state
        self.coords = coords
        self.numBuddies = 0
        self.temperature = 0

class GOL_grid(object):
    def __init__(self, position = [20,20], size=[30,30]):

        self.size = size
        self.position = position
        self.cells = []
        self.cellSize = 15
        
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

        

    def buildByString(self, _string, width=0):
        self.iterations = 0
        self.isEvolving = True

        
        counter = 0
        self.startString = _string
        numChars = len(self.startString)
        self.cells = []

        if width == 0:
            self.size[0] = int(math.sqrt(numChars))
            self.size[1] = int(self.size[0])
        else:
            self.size[0] = int(width)
            self.size[1] = int(numChars / width)

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
        borderRect = pygame.Rect(self.position[0]-3,self.position[1]-3, (self.size[0]*self.cellSize)+3,(self.size[1]*self.cellSize)+3)
        pygame.draw.rect(screen,(50,50,50), borderRect, 1)
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
        




###################
###################   SCENE EDIT
###################
###################



def cacheIteration():
    global recordCache 
    recordCache.append(grid.getString())   

def cacheRecord():
    global recordCache 
    recordCache = []
    

def buildGrid():

    grid.__init__(gridPos,[int(editWidth.getValue()),int(editHeight.getValue())])

    grid.cellSize = min( int((rightColWidth-30) / grid.size[0])  ,  int(gridMaxY/grid.size[1]))
    grid.build()      
    # oldGridString = ''
    grid.update()
    grid.isEvolving = autoPlayToggle.checked
    global frameCounter
    frameCounter = 0

def pauseGrid():

    grid.isEvolving = not grid.isEvolving


def saveRecordInCache():
    global recordString
    global recordGridWidth
    global doCache
    global cacheReady


    
    grid.buildByString(recordString, recordGridWidth)
    
    editWidth.setValue(grid.size[0])
    editHeight.setValue(grid.size[1])
    doCache = True
    cacheReady = False
    cacheRecord()


def pressListBtn(aaa, bbb, record):
    clearCache()
    global recordString
    recordString = aaa
    global recordGridWidth
    recordGridWidth = bbb    
    saveRecordInCache()

    global currentCachingRecordIterations
    currentCachingRecordIterations = record
    # grid.buildByString(aaa, bbb)

    
def clearCache():
    global recordCache
    global MODE
    global cacheReady
    global cacheLoaded
    recordCache = []
    cacheReady = False
    MODE = "SIMULATION"
    cacheLoaded = False    

def quitApp():
    global done
    done = True

MODE = "SIMULATION"
cacheLoaded = False

recordString = ''
recordGridWidth = 0
currentCachingRecordIterations = 0
pygame.init()
screen = pygame.display.set_mode((800, 700))


### dimensions for the UI
margin = 5
leftColWidth = 120
rightColWidth = screen.get_size()[0] - leftColWidth
buttonsHeight = 20
gridMaxY = 630

GOL_frameRate = 5.0
isEvolving = True




pygame.display.set_caption("Game Of Life")
ui = gui2oneUI(screen)



#####
uiY=margin
resetBtn = Button(screen, margin,uiY,leftColWidth,buttonsHeight, "Reset")
resetBtn.setFontSize(13)
resetBtn.subscribe(buildGrid)
ui.addItem(resetBtn)

uiY += margin+buttonsHeight
playBtn =  Button(screen, margin,uiY,leftColWidth,buttonsHeight, "Play")
playBtn.setFontSize(13)    
playBtn.subscribe(pauseGrid)
ui.addItem(playBtn)


uiY += margin+buttonsHeight
pauseBtn =  Button(screen, margin,uiY,leftColWidth,buttonsHeight, "Pause")
pauseBtn.setFontSize(13)    
pauseBtn.subscribe(pauseGrid)
ui.addItem(pauseBtn)

uiY += margin+buttonsHeight+10
autoPlayToggle = CheckBox(screen, margin, uiY, "Auto-play")
autoPlayToggle.checked = True
ui.addItem(autoPlayToggle)
### hide or show playBtn depending on autopPlayToggle status
playBtn.visible = not autoPlayToggle.checked

uiY += margin+buttonsHeight
clearCacheBtn = Button(screen, margin,uiY,leftColWidth,buttonsHeight, "Clear Cache")
clearCacheBtn.fontSize = 13
clearCacheBtn.visible = False
clearCacheBtn.subscribe(clearCache)
ui.addItem(clearCacheBtn)






uiY += margin+buttonsHeight
editWidth = EditText(screen, margin, uiY, 50,20,"width",90)
ui.addItem(editWidth)

uiY += margin+buttonsHeight
editHeight = EditText(screen, margin, uiY,50,20,"height",90)
ui.addItem(editHeight)




uiY += margin+buttonsHeight
listView = ListView(screen, margin,uiY,leftColWidth,300,"record list :")
ui.addItem(listView)


uiY += margin+buttonsHeight + 300
quitBtn = Button(screen, margin,uiY,leftColWidth,30, "Quit")
quitBtn.subscribe(quitApp)
ui.addItem(quitBtn)

uiY += margin+buttonsHeight + 20
cachingText = StaticText(screen, margin,uiY,leftColWidth,100,"Caching ...")
cachingText.fontSize =  20
cachingText.fontColor = (255,30,30)
cachingText.visible = False
ui.addItem(cachingText)

playModeText  = StaticText(screen, margin,uiY,leftColWidth,100,"Cache Mode")
playModeText.fontSize =  20
playModeText.fontColor = (255,30,30)
playModeText.visible = False
ui.addItem(playModeText)



record = 0
frameCounter = 0
milliCounter = 0

gridSize = int(editWidth.defaultValue)
gridPos = [leftColWidth+margin*3,margin]  
grid = GOL_grid(gridPos,[gridSize,gridSize])

timeSlider = Slider(screen, leftColWidth + margin,screen.get_height()-30,rightColWidth - (margin*2)-100,30,"time",0.0)
timeSlider.active = False
ui.addItem(timeSlider)

iterText = StaticText(screen,leftColWidth + margin*3,screen.get_height()-20,200,20)
iterText.setFontSize(13)
ui.addItem(iterText)

recordText = StaticText(screen,leftColWidth + 100+ margin*3 ,screen.get_height()-20 ,200,20)
recordText.setFontSize(13)
ui.addItem(recordText)

recordCache = []
doCache = False
cacheReady = False















buildGrid()
oldGridString = grid.getString()


clock = pygame.time.Clock()
done = False




grid.draw()


while not done:

    
    grid.cellSize = min( int((rightColWidth-30) / grid.size[0])  ,  int(gridMaxY/grid.size[1]))

    iterText.position[1] = (grid.size[1] * grid.cellSize) + iterText.size[1]
    screen.fill((0, 0, 0))


    ui.eventUpdate()


    playBtn.visible = not autoPlayToggle.checked
    ui.draw()

    if doCache:
        cachingText.visible = True
        # global timeSlider
        ratio = min(float(grid.iterations) / float(currentCachingRecordIterations),1.0)
        timeSlider.button.position[0] = timeSlider.button.dragLimits.left + (timeSlider.button.dragLimits.right-timeSlider.button.dragLimits.left) * ratio 
        
    else:
        cachingText.visible = False

    if cacheReady:
        timeSlider.active = True

        # cacheRecordBtn.visible = False
        clearCacheBtn.visible = True
        playModeText.active = True
        playModeText.visible = True
    else:
        # cacheRecordBtn.visible = False
        timeSlider.active = False   
        clearCacheBtn.visible = False
        playModeText.active = False   
        playModeText.visible = False

    if MODE == "SIMULATION":
        if record > 0:
            # cacheRecordBtn.active = True
            pass
            


        if grid.iterations % 6 == 0  and grid.iterations > 2 :
            
            newString = grid.getString()
            
            if oldGridString == newString:


                if doCache :
                    cacheReady = True
                    MODE = "CACHE"
                doCache = False
                # print "recordCache length  --> ",len(recordCache)
                grid.isEvolving = False            
                if grid.iterations-6 > record :
                    recordString = grid.startString
                    recordGridWidth = grid.size[0];
                    record = grid.iterations - 6 ### subtract same as modulo up there

                    ## adds a list item in record list
                    listView.addItem(ui,str(record), recordString)  

                    listView.items[len(listView.items)-1].subscribe(pressListBtn,recordString, grid.size[0], record)
                    

                    
                    
                buildGrid()

            else:            
                oldGridString = newString

        if(doCache):
            cacheIteration()


        grid.update()   
    
    elif MODE == "CACHE":
        cacheIndex = int(math.floor(timeSlider.getValue() * (len(recordCache)-6)))

        if not cacheLoaded:
            if cacheReady:
                cacheLoaded = True

                # grid.buildByString(recordCache[cacheIndex], recordGridWidth)
                # grid.update()
                # print "Cache Loaded...."
                # print "Length -->", len(recordCache)
        else:
            # print "-->", timeSlider.value
            grid.buildByString(recordCache[ cacheIndex], recordGridWidth)
            grid.update()
    iterText.text = "Iterations : " +str(grid.iterations)
    recordText.text = "Record : "+ str(record)

    
    grid.draw()

    
    frameCounter += 1
    

    
    clock.tick(30)
    milliCounter += clock.get_time()
    # for item in dir(clock):
    #     print item

    pygame.display.flip()
    
    
pygame.quit()