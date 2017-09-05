import Tkinter as Tk
import tkFileDialog as tkfd
import time
# import codecs
import os
import pysrt
import sys


class Phrase:

	def __init__(self):
		self.id = -1
		self.text = ""
		self.startTime = 0.0
		self.endTime = 0.0

	def __repr__(self):
		return "Phrase class :\n\tid:{}\n\ttext:{}\n\tstart time{}\n\tend time{}\n"\
			.format(self.id, self.text, self.startTime, self.endTime)


class MainApplication(Tk.Frame):

	def __init__(self, parent, *args, **kwargs):

		Tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.subs = None
		self.subData = []

		self.bShowTimer = True
		self.bTimerRunning = True

		self.masterTime = 0.0
		self.timerStartSecs = 0.0
		self.menu = Tk.Menu(self.parent)

		self.editMenu = Tk.Menu(self.menu, tearoff=0)
		self.editMenu.add_command(label="load srt file", command=self.loadSrtFile)
		self.editMenu.add_command(label="toggle timer", command=self.toggleTimer)
		self.editMenu.add_command(label="Set Start Time", command=self.setStartTimePopup)

		self.menu.add_cascade(label="edit", menu=self.editMenu)

		self.frame = Tk.Frame(self.parent)
		self.frame.pack(expand=False, fill=Tk.X)

		self.playBtn = Tk.Button(self.frame, text="pause", command=lambda: self.togglePlayTimer())
		self.playBtn["width"] = 10
		# self.playBtn["padx"] = (2, 2)

		self.playBtn.pack(side=Tk.LEFT, padx=(5, 5))

		self.restartBtn = Tk.Button(self.frame, text="restart", command=lambda: self.restartTimer())
		self.restartBtn.pack(side=Tk.LEFT, padx=(5, 5))

		self.titleTextVar = Tk.StringVar()
		self.titleTextVar.set("no file chosen")
		self.titleLabel = Tk.Label(self.frame, textvariable=self.titleTextVar)
		self.titleLabel.pack(side=Tk.RIGHT)

		self.timerTextVar = Tk.StringVar()
		self.timerTextVar.set("what ?")

		self.timeText = Tk.Label(self.parent, textvariable=self.timerTextVar, font="Helvetica, 12")

		self.timeText.width = 100
		self.timeText.pack()

		self.contentVar = Tk.StringVar()
		self.contentVar.set("content for now")

		self.contentText = Tk.Label(self.parent, textvariable=self.contentVar, font="Helvetica, 15")
		self.contentText.pack()
		self.parent.config(menu=self.menu)

		self.startTime = time.time()
		self.pauseTime = 0.0
		print self.startTime
		self.currentTime = time.time()

	def loadSrtFile(self):

		filePath = tkfd.askopenfilename(filetypes=[("Text files", "*.srt")])

		self.subs = pysrt.open(filePath)
		self.subData = []

		self.titleTextVar.set(os.path.basename(filePath))
		for sub in self.subs:

			phrase = Phrase()
			phrase.text = sub.text

			startTimeSecs = sub.start.hours * 60 * 60
			startTimeSecs += sub.start.minutes * 60
			startTimeSecs += sub.start.seconds
			phrase.startTime = startTimeSecs

			endTimeSecs = sub.end.hours * 60 * 60
			endTimeSecs += sub.end.minutes * 60
			endTimeSecs += sub.end.seconds
			phrase.endTime = endTimeSecs

			self.subData.append(phrase)

	def timerUpdate(self):

		if self.bTimerRunning:
			self.currentTime = time.time() - self.pauseTime
			self.masterTime = self.currentTime - self.startTime + self.timerStartSecs

			tempTime = self.masterTime
			# format display time
			hours = int(tempTime / (60 * 60))
			timeStr = str(hours)
			tempTime -= hours * 60 * 60

			minutes = int(tempTime / 60.0)
			timeStr += " : "
			timeStr += str(minutes)
			tempTime -= minutes * 60

			seconds = int(tempTime)
			timeStr += " : "
			timeStr += str(seconds)

			self.timerTextVar.set(str(timeStr))

		else:
			self.pauseTime = time.time() - self.currentTime
		# print self.currentTime, " -----", self.startTime

	def textUpdate(self):

		if self.bTimerRunning:

			for phrase in self.subData:
				if phrase.startTime < self.masterTime < phrase.endTime:
					self.contentVar.set(phrase.text)
					return

			self.contentVar.set("")
			pass
		else:
			pass

	def toggleTimer(self):
		self.bShowTimer = not self.bShowTimer
		if not self.bShowTimer:
			self.timeText.pack_forget()
		else:
			self.timeText.pack()

	def togglePlayTimer(self):
		self.bTimerRunning = not self.bTimerRunning
		if self.bTimerRunning:
			self.playBtn["text"] = "pause"
		else:
			self.playBtn["text"] = "play"

	def restartTimer(self):
		self.startTime = self.currentTime

	def setStartTimePopup(self):

		# tempSecs = 0.0
		toplevel = Tk.Toplevel()
		label1 = Tk.Label(toplevel, text="enter time code. ( format hh.mm.ss)", height=0, width=100)
		label1.pack()

		entry1 = Tk.Entry(toplevel)
		entry1.pack()

		def myFunc(self, top_window, entry):
			val = entry.get()
			values = val.split(".")
			if len(values) == 3:
				secs = int(values[0])*60*60
				print secs
				secs += int(values[1] * 60)
				secs += int(values[2])
				self.timerStartSecs = secs
				pass
			elif len(values) == 2:
				secs = int(values[0])*60
				secs += int(values[1])
				self.timerStartSecs = secs
				pass
			elif len(values) == 1 and values[0] != "":
				secs = int(values[0])
				self.timerStartSecs = secs
				pass
			else:
				secs = 0.0
				print " bad value entered"
			self.timerStartSecs = secs
			print self.timerStartSecs
			toplevel.destroy()

		btn = Tk.Button(toplevel, text="OK", command=lambda: myFunc(self, toplevel, entry1))
		btn.pack()


if __name__ == "__main__":

	root = Tk.Tk()
	# root.protocol("WM_DELETE_WINDOW", on_closing)
	MainApp = MainApplication(root)
	MainApp.pack(side="top", fill="both", expand=True)

	root.geometry("500x200")

	while True:
		try:
			root.update_idletasks()
			root.update()
			MainApp.timerUpdate()
			MainApp.textUpdate()
			# root.mainloop()
			time.sleep(0.01)
		except:
			sys.exit(0)
			pass

