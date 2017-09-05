import OpenGL.Tk
import tkinter as tk

class MainApplication(tk.Frame):

	def __init__(self, parent):
		self.parent = parent
		pass


if __name__ != "__main__":
	root = tk.Tk()

	mainApp = MainApplication(root)
	mainApp.pack()

	mainApp.mainloop()
