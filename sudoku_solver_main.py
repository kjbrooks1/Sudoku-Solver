#Sudoku Solver
import tkinter as tk
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
from random import randrange
import random

#global vars
MARGIN = 50
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE  * 9
GUI_GRID = {}
SOLUTION_GRID = {}
SELECTION_BAR_TEXT = []
SELECTION_BAR_RECTANGLES = []


class SudokuGUI:
    PEN = ""
    
    def __init__(self, root):
        self.root = root
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self.main_frame, bg="white", width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, expand=1)
        
        self.__draw_grid()
        self.__draw_selectionBar()

        #generate SOLUTION_GRID
        #self.fillSolutionGrid()
        #update grid we want to show user at start (GUI_GRID)
        for row in range(9):
            for col in range(9):
                GUI_GRID[(row,col)] = ""
        
        #draw the numbers in the grid
        self.__draw_puzzle()

        #buttons
        clear_button = tk.Button(self.main_frame, text="Clear", command=self.__emptyGrid(), highlightbackground="white")
        clear_button.pack(fill=BOTH, side=BOTTOM)

        #binding
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[0], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(0))   
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[1], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(1))   
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[2], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(2))   
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[3], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(3))   
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[4], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(4))   
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[5], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(5))   
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[6], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(6))   
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[7], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(7))   
        self.canvas.tag_bind(SELECTION_BAR_RECTANGLES[8], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(8))   
        
        self.canvas.tag_bind("grid", "<Button-1>", self.__cell_clicked)
        #self.canvas.bind("<Key>", self.__key_pressed)

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

                x0 = row*SIDE + MARGIN 
                y0 = col*SIDE + MARGIN
                x1 = (row+1)*SIDE + MARGIN 
                y1 = (col+1)*SIDE + MARGIN
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tag="grid")

    def __draw_selectionBar(self):
        for row in range(9):
            x0 = row*SIDE + MARGIN 
            y0 = 0*SIDE + MARGIN + 490
            x1 = (row+1)*SIDE + MARGIN 
            y1 = (1)*SIDE + MARGIN + 490
            rectobj = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
            SELECTION_BAR_RECTANGLES.append(rectobj)
            #add text
            x = row*SIDE + MARGIN + SIDE / 2 
            y = 0*SIDE + MARGIN + SIDE / 2 + 490
            tag = str(row) + "selectionBar"
            textobj = self.canvas.create_text(x, y, text=row+1, tags=tag)
            SELECTION_BAR_TEXT.append(textobj)
            
    def __draw_puzzle(self):
        #self.canvas.delete("numbers")
        for row in range(9):
            for col in range(9):
                to_fill = GUI_GRID[(row, col)]
                x = row*SIDE + MARGIN + SIDE / 2
                y = col*SIDE + MARGIN + SIDE / 2
                self.canvas.create_text(x, y, text=to_fill, tags="numbers")

    def __cell_clicked(self, event):
        x, y = event.x, event.y
        # get row and col numbers from x,y coordinates
        col, row = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
        GUI_GRID[(int(row), int(col))] = self.PEN
        self.__draw_puzzle()

    #fill board
    def fillSolutionGrid(self):
        self.emptyGrid(SOLUTION_GRID) #remove anything already there
        
        #create another dictionary with options num
        options = {}
        for row in range(9):
            for col in range(9):
                options[(row,col)] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        #pick a random square in the grid
        row = randrange(9)
        col = randrange(9)
        #put 1 there
        SOLUTION_GRID[(row, col)] = "1"
        self.removeOptions("1", row, col, options) #delete 1 from invalid places

        while(self.isFull(SOLUTION_GRID) is False):
            #find the smallest options left (besides zero)
            smallest_options = []
            shortest_length_possible = 9
            for row in range(9):
                for col in range(9):
                    if(len(options[(row,col)]) < shortest_length_possible and len(options[row,col]) > 0):
                        shortest_length_possible = len(options[(row,col)])
            for row in range(9):
                for col in range(9):
                    if(len(options[(row,col)]) == shortest_length_possible):
                        smallest_options += [(row,col)]
            #randomly select from this array and give value of smallest item in options
            if(len(smallest_options) == 0):
                if(self.isFull(SOLUTION_GRID) is False):
                    self.emptyGrid(SOLUTION_GRID)
                    self.fillSolutionGrid(SOLUTION_GRID)
                    break
            random_box = random.choice(smallest_options)
            at_row = random_box[0]
            at_col = random_box[1]
            new_value = options[random_box[0],random_box[1]][0]
            SOLUTION_GRID[(at_row,at_col)] = new_value
            self.removeOptions(new_value, at_row, at_col, options)

    #to remove numbers:
        #pick a random number you haven't tried removing
        #remove the number, run your solver with the added condition that is cannot use the removed number here
        #if the solver finds a solution, you can't remove the number
        #repeat until you have enough removed numbers (or you can't remove any more)

    '''
    def isValid(self, number, row, col, grid={}):
        #check row + col
        for x in range(9):
            if(x == row):
                pass
            if(grid[(x,col)].cget("text") == number):
                return False
        for y in range(9):
            if(y == col):
                pass
            if(grid[(row,y)].cget("text") == number):
                return False
        #check 3x3 grid
        if(row in (0,3,6) and col in (0,3,6)):
            for i in [0,1,2]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        elif(row in (0,3,6) and col in (1,4,7)):
            for i in [0,1,2]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        elif(row in (0,3,6) and col in (2,5,8)):
            for i in [0,1,2]:
                for j in [0,-1,-2]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        elif(row in (1,4,7) and col in (0,3,6)):
            for i in [-1,0,1]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        elif(row in (1,4,7) and col in (1,4,7)):
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        elif(row in (1,4,7) and col in (2,5,8)):
            for i in [-1,0,1]:
                for j in [-2,-1,0]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        elif(row in (2,5,8) and col in (0,3,6)):
            for i in [-2,-1,0]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        elif(row in (2,5,8) and col in (1,4,7)):
            for i in [-2,-1,0]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        elif(row in (2,5,8) and col in (2,5,8)):
            for i in [-2,-1,0]:
                for j in [-2,-1,0]:
                    if(i==0 and j==0):
                        pass
                    elif(grid[(row+i,col+j)].cget("text") == number):
                        return False
        else:
            print("ERROR: invalid square position")
        return True
    '''

    ####################################################
                        

    #is the 9x9 grid full?
    def isFull(self, grid={}):
        for row in range(9):
            for col in range(9):
                if(grid[(row,col)].strip() == ""):
                    return False
        return True


    #remove all other options at place and from 3x3 grid and row and col
    def removeOptions(self, numRemoving, row, col, options={}):
        options[(row,col)] = [] #remove all other options
        for x in range(9):
            if(numRemoving in options[row,x]): #remove from row
                options[row,x].remove(numRemoving)
            if(numRemoving in options[x,col]): #remove from col
                options[x,col].remove(numRemoving)
        #check 3x3 grid
        if(row in (0,3,6) and col in (0,3,6)):
            for i in [0,1,2]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        elif(row in (0,3,6) and col in (1,4,7)):
            for i in [0,1,2]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        elif(row in (0,3,6) and col in (2,5,8)):
            for i in [0,1,2]:
                for j in [0,-1,-2]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        elif(row in (1,4,7) and col in (0,3,6)):
            for i in [-1,0,1]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        elif(row in (1,4,7) and col in (1,4,7)):
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        elif(row in (1,4,7) and col in (2,5,8)):
            for i in [-1,0,1]:
                for j in [-2,-1,0]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        elif(row in (2,5,8) and col in (0,3,6)):
            for i in [-2,-1,0]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        elif(row in (2,5,8) and col in (1,4,7)):
            for i in [-2,-1,0]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        elif(row in (2,5,8) and col in (2,5,8)):
            for i in [-2,-1,0]:
                for j in [-2,-1,0]:
                    if(i==0 and j==0):
                        pass
                    elif(numRemoving in options[row+i,col+j]):
                        options[row+i,col+j].remove(numRemoving)
        else:
            print("ERROR: invalid square position")

    #connected to solve_button
    def solve(self):
        print("solved!")

    #delete all numbers from 9x9 grid
    def __emptyGrid(self):
        for row in range(9):
            for col in range(9):
                GUI_GRID[(row,col)] = ""
        self.__draw_puzzle()

    # ---------------------- EVENT HANDLER METHODS ---------------------- #
    

    def __clickedSelectionBar(self, num):
        #FFEB89 == light yellow
        anotherSelected = False
        for element in SELECTION_BAR_RECTANGLES:
            if(SELECTION_BAR_RECTANGLES.index(element) == num):
                pass
            elif(self.canvas.itemcget(element, "fill") == "#FFEB89"):
                anotherSelected = True
        if(anotherSelected == False):
            if(self.canvas.itemcget(SELECTION_BAR_RECTANGLES[num], "fill") == "#FFEB89"):
                self.canvas.itemconfig(SELECTION_BAR_RECTANGLES[num], fill="white")
                self.PEN = ""
            else:                
                self.canvas.itemconfig(SELECTION_BAR_RECTANGLES[num], fill="#FFEB89")
                self.PEN = self.canvas.itemcget(SELECTION_BAR_TEXT[num], "text")


if __name__ == "__main__":
    root = tk.Tk(className="sudoku solver")
    my_gui = SudokuGUI(root)
    root.mainloop()
