# Use Tkinter for python 2, tkinter for python 3
import Tkinter as Tk
import tkMessageBox
import ttk
import xmlrpclib
import threading
from threading import Event, Thread


class MainApplication(Tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		Tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.progress = ttk.Progressbar(self.parent)
		self.progress.pack()
		self.progress["value"] = 20
		self.progress["maximum"] = 100

		self.Hqueue = xmlrpclib.ServerProxy("http://localhost:5000")

		self.queuedJobs = self.Hqueue.getJobIdsByStatus(["queued"])



		self.counter = 0
		self.infos = Tk.Label(self.parent, text="hello" + str(self.counter))
		self.thread = self.call_repeatedly(2, self.incrementCounter)
		self.infos.pack()

		children = self.Hqueue.getJob(self.queuedJobs[0])['children']
		print "hi"
		print self.Hqueue.getJobs(children)



	def incrementCounter(self):
		self.counter += 1
		self.infos["text"] = str(self.counter)

	def set_interval(self, func, sec):
		def func_wrapper():
			self.set_interval(func, sec)
			func()
		t = threading.Timer(sec, func_wrapper)
		t.start()
		return t

	@staticmethod
	def call_repeatedly(interval, func, *args):
		stopped = Event()

		def loop():
			while not stopped.wait(interval): # the first call is in `interval` secs
				func(*args)
		Thread(target=loop).start()
		return stopped.set


def on_closing():
	if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):

		root.destroy()


if __name__ == "__main__":

	root = Tk.Tk()
	root.protocol("WM_DELETE_WINDOW", on_closing)
	MainApp = MainApplication(root).pack(side="top", fill="both", expand=True)

	root.mainloop()