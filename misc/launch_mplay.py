import subprocess
import time
import glob


path = "F:/HOUDINI_14_playground/render/i_love_this_dance/04/*"




#path = r"F:\HOUDINI_14_playground\render\wood_way\03\wood_way_with_tree_\*.exr"
formatedPath = path.replace("\\","\\\\")


while True:
	process = subprocess.Popen("C:/Program Files/Side Effects Software/Houdini 14.0.395/bin/mplay.exe -p -z 100 -r 30 F:/HOUDINI_14_playground/render/i_love_this_dance/04/_anim_04_*.exr") 

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
			print "sleep 5 seconds"
			time.sleep(60*3)

	
	print num

	#time.sleep(60*10)
	try:
		process.kill()
	except:
		print "no process to kill -- continuing"