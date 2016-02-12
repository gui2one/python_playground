
import subprocess
import time 

import os

PYTHON_PLAYGROUND = os.getenv('PYTHON_PLAYGROUND') 
# import sys




'''parameters --> launchBlender.py -- filePath | do render | 

'''
    #SUB PROCESS Render.exe
proc = subprocess.Popen('blender --python '+PYTHON_PLAYGROUND+'/blender/HOUDINI_scene_loader/launchBlender.py -- F:/HOUDINI_15_playground/lampe_colonne/lampe_colonne.xml 1',
                        shell=False,
                        stdout=subprocess.PIPE
                        )





inc = 0
while True:
	inc += 1
	output = proc.stdout.readline()
	# time.sleep(0.01)
	if ("Saved:" in output):
		print ('inc %s :  %s ' % (inc, output) )

        


 

