from PySide import QtGui
import glob
import subprocess
import time
import sys 
import threading 

class My_Thread(threading.Thread):

    def __init__(self):
		threading.Thread.__init__(self)
		self.process = None
		self.MY_GLOBAL = False
		self.CANCELED = False
		self.MPLAY_process = None        

    def run(self):

		print "Starting " + self.name
		self.CANCELED = False
		bBreak = False
		path = "F:/BLENDER_playground/*.png"
		# F:\HOUDINI_15_playground\render\fur_sea
		obj = glob.glob(path)
		newNum = len(obj)


		while True:
			'''command options *
				-T : always on top

			'''
			self.MPLAY_process = subprocess.Popen("C:/Program Files/Side Effects Software/Houdini 15.0.313/bin/mplay.exe -minimal -p -z 100 -f 1 "+str(newNum)+" 1 -r 25 F:/BLENDER_playground/*.png",shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE) 


			# print handle
			obj  = glob.glob(path)
			num = len(obj)
			oldNum = num
			

			bBreak = self.CANCELED
			while not bBreak :

				bBreak = self.MY_GLOBAL
				newNum = len(glob.glob(path))
				print newNum
				if newNum > oldNum :
					print "new file detected"
					bBreak = True

				else:
					n = 0.01
					print ("sleep %s minutes" % (n))
					print ('break -->', bBreak)
					# print process.stdin
					time.sleep(60*n)

			
			print num

			#time.sleep(60*10)
			try:
				self.MPLAY_process.kill()
				if self.CANCELED:
					print "exit while loop"
					bBreak = False
					break
			except:
				print "no process to kill -- continuing"
		print "Exiting " + self.name

    def stop(self):
        print "Trying to stop thread "
        if self.process is not None:
            self.process.terminate()
            self.process = None


class myClass(QtGui.QMainWindow):

	def __init__(self):
		self.SRCPATH = ''
		QtGui.QMainWindow.__init__(self)

		self.labelSrc = QtGui.QLabel(self)
		self.labelSrc.setText(self.SRCPATH)
		self.labelSrc.resize(300,30)
		self.labelSrc.move(10,10)

		self.choosePathButton = QtGui.QPushButton('Choose forlder', self)	
		self.choosePathButton.clicked.connect(lambda :self.choosePath())
		self.choosePathButton.move(10,40)
		self.choosePathButton.setFixedHeight(20)

		self.startButton = QtGui.QPushButton('Start MPlay', self)
		self.startButton.clicked.connect(self.threadFunction)

		self.startButton.move(10,60)

		self.cancelButton = QtGui.QPushButton('Stop MPlay', self)	
		self.cancelButton.clicked.connect(lambda :self.talk("hello"))
		self.cancelButton.move(10,60)
		self.cancelButton.hide()



		


		self.setWindowTitle("ho ho ho")
		self.setGeometry(300, 300, 680, 380)

		self.MY_GLOBAL = False
		self.CANCELED = False
		self.MPLAY_process = None
		


	def choosePath(self) :

		global SRCPATH



		# print listSrc
		# print "browse function"
		dialog = QtGui.QFileDialog(self)
		dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
		dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)   
		if dialog.exec_() :

			self.SRCPATH = dialog.selectedFiles()[0]
			# srcFolderPath = SRCPATH

			self.labelSrc.setText(self.SRCPATH)

			# os.chdir(srcFolderPath) # sets the working directory
			# fileNames = glob("*")  
			# # print fileNames           
			# model = QtGui.QStandardItemModel(self.listSrc)
			# for afile in fileNames :
			# 	# print str(afile.endswith("hdalc"))
			# 	if os.path.isfile(afile) :
			# 	    if afile.endswith("otl") | afile.endswith("hdalc") :
			# 	      item = QtGui.QStandardItem(afile)
			# 	      # item.setCheckable(True)
			# 	      item.setToolTip('self')

			# 	      model.appendRow(item)

			# 	self.listSrc.setModel(model)



	def talk(self, process):

		self.cancelButton.hide()
		self.startButton.show()
		print self.MY_GLOBAL
		self.MY_GLOBAL = True
		print(process)

		try:
			self.MPLAY_process.kill()
			self.CANCELED = True
	
		except:
			print "ou on est la ?"		

	def threadFunction(self):
		self.thread = threading.Thread(target=self.launchMplay)
		self.thread.start()


	def launchMplay(self):

		self.startButton.hide()
		self.cancelButton.show()


		self.CANCELED = False
		bBreak = False
		path = "F:/BLENDER_playground/render/world/*.png"
		# F:\HOUDINI_15_playground\render\fur_sea
		obj = glob.glob(path)
		newNum = len(obj)


		while True:

			'''command options *
				-T : always on top

			'''
			self.MPLAY_process = subprocess.Popen("C:/Program Files/Side Effects Software/Houdini 15.0.313/bin/mplay.exe -minimal -p -z 100 -f 1 "+str(newNum)+" 1 -r 25 F:/BLENDER_playground/render/world/*.png",
										shell=False,
										stdin=subprocess.PIPE,
										stdout=subprocess.PIPE) 



			obj  = glob.glob(path)
			num = len(obj)
			oldNum = num
			

			while not bBreak :

				bBreak = self.CANCELED
				newNum = len(glob.glob(path))
				print newNum
				if newNum > oldNum :
					print "new file detected"
					bBreak = True

				else:
					n = 0.05
					print ("sleep %s minutes" % (n))
					print ('break -->', bBreak)
					# print process.stdin
					time.sleep(60*n)

			
			print num

			#time.sleep(60*10)
			try:
				self.MPLAY_process.kill()
				if self.CANCELED:
					print "exit while loop"
					bBreak = False
					break
			except:
				print "no process to kill -- continuing"


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	frame = myClass()
	frame.show()

	sys.exit(app.exec_())