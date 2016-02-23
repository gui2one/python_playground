import subprocess
import time
import glob

waitTime = 0.5
path = "F:/HOUDINI_15_playground/blender_trees/render/anim_04/anim_04_*.png"
# F:\HOUDINI_15_playground\render\fur_sea
obj = glob.glob(path)
newNum = len(obj)

while True:
	### -T : always on top COMMAND
	### -minimal 
	process = subprocess.Popen("C:/Program Files/Side Effects Software/Houdini 15.0.313/bin/mplay.exe -T -minimal -p -z 133 -f 1 "+str(newNum)+" 1 -r 25 "+path) 
	

	# handle = win32gui.FindWindow(None, u"MPlay*")
	# time.sleep(10)
	# win32gui.ShowWindow(handle, 3)


	# print handle
	obj  = glob.glob(path)
	num = len(obj)
	oldNum = num
	

	bBreak = False
	while not bBreak :

		newNum = len(glob.glob(path))
		print newNum
		if newNum > oldNum :
			print "new file detected"
			bBreak = True

		else:
			n = waitTime
			print ("sleep %s minutes" % (n))
			time.sleep(60*n)

	
	print num

	#time.sleep(60*10)
	try:
		process.kill()
	except:
		print "no process to kill -- continuing"