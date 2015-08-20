import subprocess
import time
# import win32gui


path = r"F:\HOUDINI_14_playground\render\wood_way\03\wood_way_with_tree_\*.exr"
formatedPath = path.replace("\\","\\\\")
while True:
	process = subprocess.Popen("C:/Program Files/Side Effects Software/Houdini 14.0.395/bin/mplay.exe -p -z 200 F:/HOUDINI_14_playground/render/wood_way/03/wood_way_with_tree_*.exr") 

	# handle = win32gui.FindWindow(None, u"MPlay*")
	# time.sleep(10)
	# win32gui.ShowWindow(handle, 3)


	# print handle
	time.sleep(300)
	process.kill()