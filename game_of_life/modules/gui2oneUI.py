import math
import pygame
import sys

def roundValue(value, decimals = 1):
    return math.floor(value * (10 ** (decimals+1)))/ float(10 ** (decimals+1))

class Event(object):
    def __init__(self):
        self.data = "EVENT DATA"



class gui2oneUI(object):
    def __init__(self, screen):
        self.items = []
        self.screen = screen
        self.draggedItem = None
        self.isEditing = False
        self.editString = ''
        
    def addItem(self,item):
        
        if type(item).__name__ == "Slider" :

            #append empty slider container to keep data
            self.items.append(item) 
            self.items.append(item.line)
            self.items.append(item.button)

        else:
            self.items.append(item)

    def draw(self):
        for item in self.items:
            if item.parentItem != None:
                if item.parentItem.visible:
                    item.draw()            
            elif item.visible: 
                item.draw()
          
    def eventUpdate(self):
        mousePos = pygame.mouse.get_pos()
        
            
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print "bye bye"
                sys.exit()
                

            ### first, check for ediText in editMode
            for item in self.items:
                if type(item).__name__ == 'EditText':
                    if item.editMode == True:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                self.editString = ''
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                                item.editMode = False
                            else:
                                self.editString += event.unicode
                                
                            item.text = self.editString
                            item.value = item.text
                            
                            
            ### then treat the 
            for item in self.items:
                if item.active and item.visible:
                    if item.draggable:
                         
                        if self.draggedItem == None or item == self.draggedItem:
                            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1 and item.detectMouseOver(mousePos) and not item.isDragged:
                                
                                item.isDragged = True
                                
                                if self.draggedItem == None :
                                    self.draggedItem = item
                                    
                                
                            elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1  and item.isDragged:
                                if item == self.draggedItem:                    
                                    if item.dragDir == "horizontal" :

                                        item.position = [item.position[0]+event.rel[0], item.position[1]]
                                        if item.parentItem != None :
                                            item.parentItem.value = item.getValue()
                                            
                                        
                                        if item.position[0] < item.dragLimits.left:
                                            item.position[0] = item.dragLimits.left
                                        elif item.position[0] > item.dragLimits.right:
                                            item.position[0] = item.dragLimits.right
                                            
                                    elif item.dragDir == "vertical":
                                        item.position = [item.position[0], item.position[1]+event.rel[1]]

                                        if item.position[1] < item.dragLimits.top:
                                            item.position[1] = item.dragLimits.top
                                        elif item.position[1] > item.dragLimits.bottom:
                                            item.position[1] = item.dragLimits.bottom                                    
                            else :
                                item.isDragged = False
                                self.draggedItem = None

                    else:            
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            ##print pygame.event.event_name(event.type)                
                        elif event.type == pygame.MOUSEMOTION :
                            if type(item).__name__ == 'Button' and item.detectMouseOver(mousePos):
                                #print type(item).__name__, item.name
                                item.color = (200,200,30)
                                item.isMouseOver = True
                            else:
                                item.color = (150,150,150)
                                item.isMouseOver = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if type(item).__name__ == 'Button' and item.detectMouseOver(mousePos):
                                # print "Button --> ", item.name
                                item.color = (200,30,200)
                                item.isClicked = True
                                item.fire()
                            elif type(item).__name__ == 'EditText' and item.detectMouseOver(mousePos):
                                # print "clicked EditText"
                                item.editMode = True
                            elif type(item).__name__ == 'CheckBox' and item.detectMouseOver(mousePos):                                
                                item.checked = not item.checked
                            else:
                                item.color = (150,150,150)
                                item.isClicked = False
                                
                                
                                if type(item).__name__ == 'EditText':
                                    # if item.editMode : print item.getValue()
                                    item.editMode = False
                                    self.editString = ''
                           
                
                    
                
class uiItem(object):
    def __init__(self,screen,x,y,width, height,name,defaultValue,draggable,dragDir,fontSize):

        self.visible = True
        self.active = True
        self.showLabel = False
        self.name = name
        self.screen = screen
        self.draggable = draggable
        self.dragDir = dragDir
        self.isDragged = False
        self.position = [x,y]
        self.size = [width,height]
        self.rect = pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])
        self.dragLimits = self.rect
        self.parentItem = None

        self.fontSize = fontSize
        self.fontColor = (255,255,255)
        self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        self.fontScale = 1.0
        
        self.defaultValue = defaultValue
        self.value = self.defaultValue


        self.isMouseOver = False
        self.isClicked = False
        self.callbacks = []
        self.callbacksArgs = []
        
    def subscribe(self, callback,*attrs):
        # print "ATTRS -->", attrs
        self.callbacks.append(callback)
        self.callbacksArgs.append(attrs)
        
    def fire(self, *args):
        # print "ARGS -->", args
        e = Event()
        # print "attr -->", attrs
        # for k, v in attrs.iteritems():
        #     setattr(e, k, v)
        #     print k
        for i,fn in enumerate(self.callbacks):
            if len(self.callbacksArgs) > 0:
                fn(*self.callbacksArgs[i])
            else:
                fn()
                
    def setFontSize(self, fSize):
        self.fontSize = fSize
           

    def setSize(self, width , height):
        self.size = [width,height]

    def getValue(self):

        
        if type(self).__name__ == 'Button' and self.parentItem != None: 
            val = (self.position[0] - self.dragLimits.left) / float(self.dragLimits.right - self.dragLimits.left)
            if val < 0.0 :val = 0.0
            elif val > 1.0:val = 1.0
            
            self.value = val 
            return val

        elif type(self).__name__ == 'Slider': 
            val = (self.button.position[0] - self.button.dragLimits.left) / float(self.button.dragLimits.right - self.button.dragLimits.left)
            if val < 0.0 :val = 0.0
            elif val > 1.0:val = 1.0
            
            self.value = val  
            return val            
        elif type(self).__name__ == 'EditText':
            val = self.text
            return val
    
    def setValue(self, val):
        self.value = val

    def detectMouseOver(self,mouse):
        if mouse[0] > self.position[0] and mouse[1] > self.position[1] and mouse[0] < self.position[0] + self.size[0] and mouse[1] < self.position[1] + self.size[1]:
            return True
        else:            
            return False    


class StaticText(uiItem):
    def __init__(self, screen, x,y,width, height,name="item_name",defaultValue=0.0 , draggable=False, dragDir="horizontal",fontSize=12):
        uiItem.__init__(self,screen,x,y,width, height,name,defaultValue,draggable=False, dragDir="horizontal", fontSize=12)
        self.text = name
        self.fontSize = fontSize
    
    def draw(self):
        self.rect = pygame.Rect(self.position[0],self.position[1], self.size[0], self.size[1])
        self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        textSurface = self.font.render(self.text, True, self.fontColor)
        
        textPosX = self.rect.left
        textPosY = self.rect.top        
        self.screen.blit(textSurface,(textPosX,textPosY))  

class EditText(uiItem):
    def __init__(self, screen, x,y,width, height,name="item_name",defaultValue=0.0 , draggable=False, dragDir="horizontal",fontSize=12):
        uiItem.__init__(self,screen,x,y,width, height,name,defaultValue,draggable=False, dragDir="horizontal", fontSize=12)

        self.showLabel = True
        self.text = str(defaultValue)
        self.editMode = False

    def draw(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        offsetX = 0
        self.text = str(self.value)

 
        
        
        textSurface = self.font.render(self.text, True, (255,255,255))
        surfSize = textSurface.get_size()
        
        textPosX = self.rect.left + ( (self.size[0] - surfSize[0])/2.0)
        textPosY = self.rect.top  + ( (self.size[1] - surfSize[1])/2.0) 

        if self.showLabel:
            labelSurface = self.font.render(str(" : "+self.name ), True, (255,255,255))
            offsetX = self.size[0]+5
            labelPosX = self.rect.left+offsetX
            labelPosY = self.rect.top  + ( (self.size[1] - labelSurface.get_size()[1])/2.0)
            self.screen.blit(labelSurface,(labelPosX,labelPosY))

        borderRect = pygame.Rect(self.position[0],self.position[1],self.size[0], self.size[1])
        pygame.draw.rect(self.screen, (255,255,255), borderRect,1)

        if self.editMode : pygame.draw.rect(self.screen, (50,50,100), pygame.Rect(textPosX, textPosY, surfSize[0], surfSize[1]))
   
        self.screen.blit(textSurface,(textPosX,textPosY))          

class Line(uiItem):
    def __init__(self, screen, x,y,width, height,name="item_name",defaultValue=0.0 , draggable=False, dragDir="horizontal",fontSize=12):
        uiItem.__init__(self,screen,x,y,width, height,name,defaultValue,draggable=False, dragDir="horizontal",fontSize=12)
        self.color = (55,55,55)
        self.fontSize = fontSize
        self.showLabel = False
  
    def draw(self):
        self.rect = pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])
        pygame.draw.rect(self.screen, self.color, self.rect)
        if self.showLabel:
            self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
            textSurface = self.font.render(self.name, True, (255,255,255)) 
            textPosX = self.rect.left
            textPosY = self.rect.top
            
            self.screen.blit(textSurface,(textPosX,textPosY))        
        
class Slider(uiItem):
    def __init__(   self, screen,x,y,width, height,name="item_name",defaultValue=0.0,draggable=False,dragDir="horizontal",fontSize=12):
        
        uiItem.__init__(self,screen,x,y,width, height,name,defaultValue, draggable=False, dragDir="horizontal",fontSize=12)
        self.color = pygame.Color("#555555")
   
        self.line = Line( screen, self.position[0], self.position[1], self.size[0],2, self.name)
        self.line.color = pygame.Color("gray")
        self.line.parentItem = self

        self.button = Button(screen, self.position[0], self.position[1]-6, 12,12,"")
        self.button.dragLimits = pygame.Rect(self.position[0], self.position[1], self.size[0],20)
        
        self.button.position[0] = (self.defaultValue *  self.size[0] ) + self.position[0]
        self.button.draggable = True
        self.button.parentItem = self
      
    def draw(self):
        
        self.button.active = self.active
        # self.button.position = [ self.button.position[0], self.button.position[1]]
        textSurface = self.font.render(str(roundValue(self.value)), True, (255,255,255))
        self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        textPosX = self.rect.right+15
        textPosY = self.rect.top-7
        self.screen.blit(textSurface,(textPosX,textPosY))   

 
        
class Button(uiItem):    
    def __init__(self, screen, x,y,width, height,name="item_name", defaultValue=0.0,draggable=False, dragDir="horizontal",fontSize=12):
        uiItem.__init__(self,screen,x,y,width, height, name, defaultValue,draggable=False, dragDir="horizontal",fontSize=12)

        self.color = (255,20,20)        
        self.text = self.name
    
    def draw(self):
        self.rect = pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])
        pygame.draw.rect(self.screen, self.color,self.rect)
        
        self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        textSurface = self.font.render(self.text, True, (255,255,255))        
        textPosX = self.rect.centerx - (textSurface.get_width()/2.0)
        textPosY = self.rect.centery - (textSurface.get_height()/2.0)
        
        self.screen.blit(textSurface,(textPosX,textPosY))

class ListView(uiItem):
    def __init__(self, screen, x,y,width, height,name="item_name", defaultValue=0.0,draggable=False, dragDir="horizontal",fontSize=12):
        uiItem.__init__(self,screen,x,y,width, height, name, defaultValue,draggable=False, dragDir="horizontal",fontSize=12)
        self.items = []
        self.values = []

    def addItem(self,ui,itemName, itemValue=None):
        offsetY = len(self.items) * 20
        button = Button(self.screen,self.position[0],self.position[1] + offsetY + 15,self.size[0],20,itemName)
        ui.items.append(button)
        self.items.append(button)
        self.values.append(itemValue)

    def draw(self):

        self.rect = pygame.Rect(self.position[0],self.position[1]+15,self.size[0],self.size[1])
        pygame.draw.rect(self.screen, self.color,self.rect)
        
        self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        textSurface = self.font.render(self.name, True, (255,255,255))        
        textPosX = self.rect.left + 5
        textPosY = self.rect.top - 15
        
        self.screen.blit(textSurface,(textPosX,textPosY))            

        # for i, item in enumerate(self.items):
        #     textSurface = self.font.render(item.name, True, (255,255,255))  
        #     offsetY = (i * 20) + 10
        #     textPosX = self.rect.left + 20
        #     textPosY = self.rect.top + offsetY
            
        #     self.screen.blit(textSurface,(textPosX,textPosY)) 

class CheckBox(uiItem):
    def __init__(self, screen, x,y,name="item_name", defaultValue=0.0,draggable=False, dragDir="horizontal",fontSize=12):
        self.size = [30,30]
        uiItem.__init__(self,screen,x,y,self.size[0], self.size[1], name, defaultValue,draggable=False, dragDir="horizontal",fontSize=12)

        self.color = (255,20,20)        
        self.text = self.name 
        self.size = [10,10]
        self.checked = False
        
    def draw(self):
        self.rect = pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])

        if self.checked :
            pygame.draw.rect(self.screen, self.color,self.rect)
        
        pygame.draw.rect(self.screen, (255,255,255),self.rect,1) 

        
        self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        textSurface = self.font.render(self.text, True, (255,255,255))        
        textPosX = self.rect.left + 30
        textPosY = self.rect.centery - (textSurface.get_height()/2.0)
        
        self.screen.blit(textSurface,(textPosX,textPosY))        


def main():
    if(__name__ != "__main__"):
        main()

    
