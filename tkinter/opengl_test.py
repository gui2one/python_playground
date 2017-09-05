import OpenGL.Tk
import Tkinter as Tk

class MainApplication(Tk.Frame):

	def __init__(self):
		pass


if __name__ != "__main__":
	root = Tk.Tk()

	mainApp = MainApplication(root)
	mainApp.pack()

	mainApp.mainloop()

