import subprocess
import time
# import win32gui



while True:
	process = subprocess.Popen("C:\\Program Files\\Side Effects Software\\Houdini 14.0.395\\bin\\mplay.exe -p F:\\HOUDINI_14_playground\\render\\tortured_tree\\01\\* " )

	# handle = win32gui.FindWindow(None, u"MPlay*")
	# time.sleep(10)
	# win32gui.ShowWindow(handle, 3)


	# print handle
	time.sleep(300)
	process.kill()