from visual import *


scene2 = display(title='Examples of Tetrahedrons',
     x=0, y=0, width=960, height=540,
     center=(0,0,5), background=(0,1,1))
sphere1 = sphere()
sphere1.radius = 0.5

sphere2 = sphere()
sphere2.radius = 0.5
sphere2.pos = (3,0,0)