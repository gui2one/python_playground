import Cell
import random as rand
'''Mine Sweeper Grid Class'''

class Grid(object):

    def __init__(self, canvas, width, height, cells_size):
        self.width = width
        self.height = height
        self.canvas = canvas
        self.cells_size = cells_size
        self.cells = []
        self.create()

        
    def create(self):
        id = 0
        for y in range(self.height):
            for x in range(self.width):
                rand_val = rand.uniform(0, 1) > 0.9
                cell = Cell.Cell(
                    self.canvas, x, y, self, size=self.cells_size, cell_id=id, has_mine=rand_val)

                self.cells.append(cell)
                # print x, y
                id += 1

    def check_neighbours(self,cell_id):
        '''
        checking neighbours for mines
        '''
        num_mines = 0
        print self.cells[cell_id].has_mine

        return num_mines
        

