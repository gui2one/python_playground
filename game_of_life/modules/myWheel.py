import pygame
import math

class myWheel():
    def __init__(self,_screen, parent=None):
        self.screen = _screen
        self.position = [50,200]
        self.radius = 30.0
        self.segs = 10
        self.rotation = 0.0
        self.reverse = False
        self.parent = parent
        self.radialOffset = 0.0

    def setParent(self,parent):
        self.parent = parent
        #print self.parent.parent

    def setPosition(self,x,y):
        self.position = [x,y]

    def setRotation(self, offset):

        if self.parent != None :
            ###
            ########
            ##################
            ########################      VICTOIRE ?!!!
            ##################
            ########
            ###
            perimeter = math.pi *2.0 * self.radius
            parentPerimeter = math.pi *2.0* self.parent.radius
            #print self.radius, self.parent.radius
            self.rotation = (-self.parent.rotation * ( float(self.parent.radius)/self.radius))

            ## find what distance does radialOffset represents on the parent circle.
            val = (parentPerimeter * self.radialOffset)
            self.rotation += ((self.radialOffset * math.pi * 2.0)  ) *(1 + (parentPerimeter/perimeter))
            
        else:
            if self.reverse : offset *= -1
            self.rotation = ((-offset *(math.pi*2.0)/ (math.pi*2*self.radius)))

    def draw(self):
        points = []      
        
        if self.parent != None :
            radianVal = self.radialOffset * math.pi*2.0
            self.position = [self.parent.position[0] + math.sin(radianVal) * (self.radius + self.parent.radius) , self.parent.position[1] +math.cos(radianVal) * (self.radius + self.parent.radius)  ];
        for i in range(0,self.segs+1):
                
            angleRad = (((math.pi*2.0) / float(self.segs)) * i) + self.rotation
            posX = (math.sin(angleRad)* self.radius) + self.position[0]
            posY = (math.cos(angleRad)* self.radius) + self.position[1]
            points.append([posX, posY])

        ## add a last vertex at center
        points.append(self.position)
        poly = pygame.draw.polygon(self.screen,(20,255,10),points,1)
        




def main():


    if __name__ != "__main__":
        main()
