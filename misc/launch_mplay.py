import subprocess
import time
import glob


path = "F:/HOUDINI_15_playground/render/fur_sea/*"
# F:\HOUDINI_15_playground\render\fur_sea
obj = glob.glob(path)
newNum = len(obj)

while True:
	process = subprocess.Popen("C:/Program Files/Side Effects Software/Houdini 15.0.244.16/bin/mplay.exe -p -z 133 -f 1 "+str(newNum-1)+" 1 -r 25 F:/HOUDINI_15_playground/render/fur_sea/fur_sea_*.exr") 
	

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
			n = 1
			print ("sleep %s minutes" % (n))
			time.sleep(60*n)

	
	print num

	#time.sleep(60*10)
	try:
		process.kill()
	except:
		print "no process to kill -- continuing"