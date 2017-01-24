import pygame
import math
pygame.init()
pygame.key.set_repeat(300,50)
screen = pygame.display.set_mode((600, 500))
done = False
is_blue = True
posx = screen.get_width()/2.0
time = 0.0
clock = pygame.time.Clock()

paused = False
SPEED = 1.0
speedMult = 1.0;
RADIUS_MULT = 1.0
##for item in dir(clock):
##    print item


class myWheel():
    def __init__(self):
        self.position = [50,50]
        self.radius = 30.0
        self.segs = 20
        self.rotation = 0.0
        self.reverse = False
        

    def setPosition(self,x,y):
        self.position = [x,y]

    def setRotation(self, offset):
        if self.reverse : offset *= -1
        self.rotation = ((-offset *(math.pi*2.0)/ (math.pi*2*self.radius)))

    def draw(self):
        points = []


        
        for i in range(0,self.segs+1):
                
            angleRad = (((math.pi*2.0) / float(self.segs)) * i) + self.rotation
            posX = (math.sin(angleRad)* self.radius) + self.position[0]
            posY = (math.cos(angleRad)* self.radius) + self.position[1]
            points.append([posX, posY])

        ## add a last vertex at center
        points.append(self.position)
        poly = pygame.draw.polygon(screen,(20,255,10),points,1)
        





    
print dir(myWheel)


class Button():
    def __init__(self,x,y,name="button_instance"):
        self.position = [x,y]
        self.color = (255,20,20)
        self.name = name
        

    def draw(self):

        self.rect = pygame.draw.rect(screen, self.color,(self.position[0],self.position[1],50,50))

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        
                        return True
                        
                    else:                        
                        return False
                else:                   
                    return False
            else:                
                return False
        else:            
            return False


btn1 = Button(20,20,"btn_one")
btn2 = Button(20,200,"btn_two")    
while not done:
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn1.pressed(pygame.mouse.get_pos()):
                        btn1.color = (20,255,20)
                        RADIUS_MULT += 0.1
                        print btn1.name
                    else:
                        btn1.color = (255,20,20)
                    if btn2.pressed(pygame.mouse.get_pos()):
                        btn2.color = (20,255,20)
                        RADIUS_MULT -= 0.1
                        print btn2.name
                    else:
                        btn2.color = (255,20,20)                        
                if event.type == pygame.QUIT:
                        done = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        is_blue = not is_blue
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        paused = not paused
                        if paused :
                            speedMult = 0.0
                        else:
                            speedMult = 1.0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP_PLUS:
                        SPEED += 0.1
                        #print SPEED
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP_MINUS:
                        SPEED -= 0.1
                        #print SPEED
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: y -= 3
        if pressed[pygame.K_DOWN]: y += 3
        if pressed[pygame.K_LEFT]: x -= 3
        if pressed[pygame.K_RIGHT]: x += 3
        
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)

        
        time += clock.get_time()*0.0005 * SPEED * speedMult

        offsetx = (math.cos(time)*200.0) + posx
        screen.fill((0, 0, 0))
        
        btn1.draw()
        btn2.draw()
        
    
        radii = [5,10,20,40,60,80]
        
        for n in range(0, len(radii)):
            
            radii[n]= radii[n] * RADIUS_MULT
            
        toggleReverse = False
        offsety = 0.0
        
        for i in range(0,len(radii)):

            if i != 0:
                offsety += radii[i-1]+ radii[i]
            else:
                offsety += radii[i]
            obj = myWheel()
            obj.radius = radii[i]
            obj.segs = 15
            obj.setPosition(offsetx,offsety)
            obj.reverse = toggleReverse
            obj.setRotation(offsetx)
            
            obj.draw()
            toggleReverse = not toggleReverse

            
        pygame.display.flip()
        # will block execution until 1/60 seconds have passed 
        # since the previous time clock.tick was called. 
        clock.tick(30)        


pygame.quit()
