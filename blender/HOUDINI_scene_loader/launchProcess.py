
import subprocess
import time 

import os

PYTHON_PLAYGROUND = os.getenv('PYTHON_PLAYGROUND') 
# import sys




'''parameters --> launchBlender.py -- filePath | do render | 

'''
    #SUB PROCESS Render.exe
proc = subprocess.Popen('blender --python '+PYTHON_PLAYGROUND+'/blender/HOUDINI_scene_loader/launchBlender.py -- Z:/HOUDINI_15_playground/HoudiniToBlenderProject.xml 0',
                        shell=True,
                        stdout=subprocess.PIPE
                        )





inc = 0
while True:
    inc += 1
    output = proc.stdout.readline()
    # time.sleep(0.01)
    # if ("frame " in output) or ("::::" in output) :

    print ('inc %s :  %s ' % (inc, output) )

        


 

