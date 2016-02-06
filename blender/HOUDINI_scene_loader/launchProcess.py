
import subprocess
import time 

 
# import sys


#SUB PROCESS Render.exe
proc = subprocess.Popen('blender --python F:/PYTHON_playground/blender/HOUDINI_scene_loader/launchBlender.py -- F:/HOUDINI_15_playground/World_scene.xml',
                        shell=True,
                        stdout=subprocess.PIPE
                        )


# while True:
#     stdout_value = proc.stdout.readline()
#     line  = stdout_value
#     print 'stdout: %s' % (line)
inc = 0
while True:
    inc += 1
    output = proc.stdout.readline()
    time.sleep(0.01)
    if ("frame " in output) or ("::::" in output) :

        print ('inc %s :  %s ' % (inc, output) )

        


 

