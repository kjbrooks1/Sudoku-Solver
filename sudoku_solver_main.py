#Sudoku Solver
import tkinter as tk
from tkinter import Canvas, BOTH, BOTTOM
from random import randrange
import random

'''
isValid is totally fucked up!!!
'''

#global vars
MARGIN = 50
SIDE = 50
WIDTH = MARGIN * 2 + SIDE  * 9
HEIGHT = WIDTH + 100


SOLUTION_GRID = {}

SELECTION_BAR_TEXT = []
SELECTION_BAR_RECTANGLES = []

USER_VISIBLE_TEXT_OBJECTS = {}

class SudokuGUI:
    PEN = ""
    CURRENT_GRID = {}

    def __init__(self, root):
        self.root = root

        self.canvas = Canvas(self.root, bg="white", width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, expand=1)
        
        self.__draw_grid()
        self.__draw_selectionBar()

        #generate SOLUTION_GRID
        #self.fillSolutionGrid()

        #update grid we want to show user at start (CURRENT_GRID)
        testing_grid = [
            [" ", " ", " ", "2", "6", " ", "7", " ", "1"],
            ["6", "8", " ", " ", "7", " ", " ", "9", " "],
            ["1", "9", " ", " ", " ", "4", "5", " ", " "],
            ["8", "2", " ", "1", " ", " ", " ", "4", " "],
            [" ", " ", "4", "6", " ", "2", "9", " ", " "],
            [" ", "5", " ", " ", " ", "3", " ", "2", "8"],
            [" ", " ", "9", "3", " ", " ", " ", "7", "4"],
            [" ", "4", " ", " ", "5", " ", " ", "3", "6"],
            ["7", " ", "3", " ", "1", "8", " ", " ", " "]    ]

        for row in range(9):
            for col in range(9):
                self.CURRENT_GRID[(row,col)] = testing_grid[row][col]
        
        #draw the numbers in the grid
        self.__draw_puzzle()

        #buttons
        clear_button = tk.Button(self.root, text="Clear", command=lambda: self.__emptyGrid(), highlightbackground="white")
        clear_button.pack(fill=BOTH, side=BOTTOM)
        solver_button = tk.Button(self.root, text="Run Solver", command=lambda: self.__run_solver(0,0), highlightbackground="white")
        solver_button.pack(fill=BOTH, side=BOTTOM)

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
        self.canvas.tag_bind(SELECTION_BAR_TEXT[0], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(0))   
        self.canvas.tag_bind(SELECTION_BAR_TEXT[1], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(1))   
        self.canvas.tag_bind(SELECTION_BAR_TEXT[2], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(2))   
        self.canvas.tag_bind(SELECTION_BAR_TEXT[3], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(3))   
        self.canvas.tag_bind(SELECTION_BAR_TEXT[4], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(4))   
        self.canvas.tag_bind(SELECTION_BAR_TEXT[5], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(5))   
        self.canvas.tag_bind(SELECTION_BAR_TEXT[6], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(6))   
        self.canvas.tag_bind(SELECTION_BAR_TEXT[7], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(7))   
        self.canvas.tag_bind(SELECTION_BAR_TEXT[8], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(8))  
        
        self.canvas.tag_bind("grid", "<Button-1>", self.__cell_clicked)
        #add function so key nums change selection bar
        
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
            rectobj = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", tags="selectionBar")
            SELECTION_BAR_RECTANGLES.append(rectobj)
            #add text
            x = row*SIDE + MARGIN + SIDE / 2 
            y = 0*SIDE + MARGIN + SIDE / 2 + 490
            textobj = self.canvas.create_text(x, y, text=row+1, tags="selectionBar")
            SELECTION_BAR_TEXT.append(textobj)
            
    def __draw_puzzle(self):
        #self.canvas.delete("numbers")
        for row in range(9):
            for col in range(9):
                to_fill = self.CURRENT_GRID[(row,col)]
                x = col*SIDE + MARGIN + SIDE / 2
                y = row*SIDE + MARGIN + SIDE / 2
                box = self.canvas.create_text(x, y, text=to_fill, tags="grid")
                USER_VISIBLE_TEXT_OBJECTS[(row, col)] = box

    def __update_puzzle(self, row, col, newNum):
        self.CURRENT_GRID[(row, col)] = str(self.PEN)
        self.canvas.itemconfig(USER_VISIBLE_TEXT_OBJECTS[(row, col)], text=newNum, fill="blue")

    def print_current_grid(self):
        for row in range(9):
            if(row % 3 == 0):
                print("-------------------------")
            print(self.CURRENT_GRID[(row,0)],self.CURRENT_GRID[(row,1)],self.CURRENT_GRID[(row,2)]," | ",
                self.CURRENT_GRID[(row,3)],self.CURRENT_GRID[(row,4)],self.CURRENT_GRID[(row,5)]," | ",
                self.CURRENT_GRID[(row,6)],self.CURRENT_GRID[(row,7)],self.CURRENT_GRID[(row,8)])
        print("-------------------------")

    #delete all numbers from 9x9 grid
    def __emptyGrid(self):
        for row in range(9):
            for col in range(9):
                self.__update_puzzle(row, col, "")
                
    # ---------------------- EVENT HANDLER METHODS ---------------------- #
    def __cell_clicked(self, event):
        x, y = event.x, event.y
        # get row and col numbers from x,y coordinates
        col, row = (x - MARGIN) / SIDE, (y - MARGIN) / SIDE
        self.__update_puzzle(int(row), int(col), self.PEN)

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
    
    def __run_solver(self, masterRow, masterCol): #w/backtracking, recursion
        #base case - no more rows or columns
        if(masterRow == 8 and masterCol == 9):
            return True

        #end of row, move to next
        if(masterCol == 9):
            masterRow += 1
            masterCol = 0

        current_cell = self.canvas.itemcget(USER_VISIBLE_TEXT_OBJECTS[(masterRow, masterCol)], "text").strip()
        #if something already there, move on
        if(current_cell != ""):
            return self.__run_solver(masterRow, masterCol+1)

        for num in range(1,10): #try all options until one doesn't break the board
            if(self.isValid(num, masterRow, masterCol)):
                #true is safe, so fill grid space
                self.CURRENT_GRID[(masterRow,masterCol)] = str(num)
                self.canvas.itemconfig(USER_VISIBLE_TEXT_OBJECTS[(masterRow, masterCol)], text=str(num), fill="green")

                self.print_current_grid()

                if(self.__run_solver(masterRow, masterCol+1)):
                    return True

                self.CURRENT_GRID[(masterRow,masterCol)] = " "
                self.canvas.itemconfig(USER_VISIBLE_TEXT_OBJECTS[(masterRow, masterCol)], text=" ", fill="green")
        return False

    def isValid(self, number, row, col):
        number = str(number)
        #check row + col
        for x in range(9):
            if(x == col):
                pass
            elif(self.CURRENT_GRID[(row,x)] == number):
                return False
        for y in range(9):
            if(y == row):
                pass
            elif(self.CURRENT_GRID[(y,col)] == number):
                return False
        #check 3x3 grid
        if(row in (0,3,6) and col in (0,3,6)):
            for i in [0,1,2]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        elif(row in (0,3,6) and col in (1,4,7)):
            for i in [0,1,2]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        elif(row in (0,3,6) and col in (2,5,8)):
            for i in [0,1,2]:
                for j in [0,-1,-2]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        elif(row in (1,4,7) and col in (0,3,6)):
            for i in [-1,0,1]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        elif(row in (1,4,7) and col in (1,4,7)):
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        elif(row in (1,4,7) and col in (2,5,8)):
            for i in [-1,0,1]:
                for j in [-2,-1,0]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        elif(row in (2,5,8) and col in (0,3,6)):
            for i in [-2,-1,0]:
                for j in [0,1,2]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        elif(row in (2,5,8) and col in (1,4,7)):
            for i in [-2,-1,0]:
                for j in [-1,0,1]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        elif(row in (2,5,8) and col in (2,5,8)):
            for i in [-2,-1,0]:
                for j in [-2,-1,0]:
                    if(i==0 and j==0):
                        pass
                    elif(self.CURRENT_GRID[(row+i,col+j)] == number):
                        return False
        else:
            print("ERROR: invalid square position")
        return True
    
    # ------------ TO UPDATE LATER ------------ # 

    def isFull(self):
        for row in range(9):
            for col in range(9):
                if(self.CURRENT_GRID[(row,col)].strip() == ""):
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

    def fillSolutionGrid(self):
        self.__emptyGrid() #remove anything already there
        
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

        while(self.isFull() is False):
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
                if(self.isFull() is False):
                    self.__emptyGrid()
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

if __name__ == "__main__":
    root = tk.Tk(className="sudoku solver")
    my_gui = SudokuGUI(root)
    root.mainloop()
