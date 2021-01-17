#Sudoku Solver
import tkinter as tk
from tkinter import Canvas, BOTH

class SudokuGUI:

    MARGIN = 50
    SIDE = 50
    WIDTH = MARGIN*2  + SIDE*9

    def __init(self, root):
        self.root = root
        
        self.canvas = Canvas(self.root, bg="white")
        self.canvas.pack(fill=BOTH, expand=1)

        self.__draw_gird()
    
    def __draw_grid(self):
        for row in range(9):
            for col in range(9):
                color = "white"
                if(row in (0,1,2) and col in (3,4,5)):
                    color = "light grey"
                elif(row in (6,7,8) and col in (3,4,5)):
                    color = "light grey"
                elif(row in (3,4,5) and col in (0,1,2,6,7,8)):
                    color = "light grey"

                x0 = col*self.SIDE + self.MARGIN 
                y0 = row*self.SIDE + self.MARGIN
                x1 = (col+1)*self.SIDE + self.MARGIN 
                y1 = (row+1)*self.SIDE + self.MARGIN
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tag="grid")