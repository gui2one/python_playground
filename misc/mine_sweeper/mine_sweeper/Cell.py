"""This module creates a Cell object for Mine Sweeper game"""

class Cell(object):
    '''Mine Sweeper Cell class'''

    def __init__(self, canvas, x, y, grid, size=20, cell_id=0, has_mine=False):
        self.grid = grid
        self.x_pos = x
        self.y_pos = y
        self.coords = [x,y]
        self.size = size
        self.num_mines_around = 0
        self.canvas = canvas
        self.cell_id = cell_id
        self.has_mine = has_mine
        self.cell = self.create_cell()
        self.canvas.tag_bind(self.cell, '<ButtonPress-1>', self.on_left_click)
        self.canvas.tag_bind(self.cell, '<ButtonPress-3>', self.on_right_click)

    def set_has_mine(self, value):
        '''
        sets the has_mine state of the cell --> boolean value
        '''
        self.has_mine = value


    def on_left_click(self, event):
        '''manage click event'''
        event.widget.itemconfig(self.cell, fill="yellow", activefill="")
        # self.grid.check_neighbours(self.cell_id)

        if self.has_mine :
            print "You blew up !!! Sorry"
        else:
            print "you survived this time ...."
        # print 'left click'

    def on_right_click(self,event):
        '''right click event'''
        event.widget.itemconfig(self.cell, fill="green", activefill="")
        # print 'right click'



    def create_cell(self):
        '''creating cell polygon'''
        cell = self.canvas.create_polygon(self.x_pos * self.size, self.y_pos * self.size,
                                          (self.x_pos + self.size) * self.size, self.y_pos * self.size,
                                          (self.x_pos + self.size) * self.size, (self.y_pos + self.size) * self.size,
                                          self.x_pos * self.size, (self.y_pos + self.size)* self.size,
                                          tags="cell", fill="grey", outline="white",
                                          activefill="lightgrey")
        
        if self.has_mine :
            self.canvas.itemconfig(cell, fill="red", activefill="")

        return cell
    
