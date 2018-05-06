'''Mine Sweeper Game'''

import os
import sys
import Tkinter as tk

modulePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mine_sweeper")
sys.path.append(modulePath)
import Grid

TOP = tk.Tk()



GRID_WIDTH = 20
GRID_HEIGHT = 20

CELL_SIZE = 30
# Code to add widgets will go here...
CANVAS = tk.Canvas(TOP, bg="blue", height=GRID_HEIGHT * CELL_SIZE, width=GRID_WIDTH * CELL_SIZE)



grid = Grid.Grid(CANVAS, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)

CANVAS.pack()

TOP.mainloop()
