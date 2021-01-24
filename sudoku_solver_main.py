#Sudoku Solver
#Katherine Brooks

import tkinter as tk
from tkinter import Canvas, RIGHT, Y, LEFT
import tkinter.font as tkFont
from random import randrange
import random

'''
Things I want to add:
- dark/light mode switch
- pen vs. pencil functionality
- clear only user added nums
- clear only solver's added nums
- user click can't remove given numbers
- use solver to make puzzles from solution grid method
- get a hint
- difficulty setting
'''


class SudokuGUI:

    #GUI vars
    MARGIN = 50
    SIDE = 50
    WIDTH = MARGIN * 2 + SIDE  * 9
    HEIGHT = MARGIN * 2 + SIDE  * 9 + 100
    
    #grid vars
    CURRENT_GRID = {}
    SOLUTION_GRID = {}

    #other
    SELECTION_BAR_TEXT = []
    SELECTION_BAR_RECTANGLES = []
    USER_VISIBLE_TEXT_OBJECTS = {}
    PEN = ""

    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(self.root, bg="white", width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(fill=Y, side=RIGHT, expand=1)
        
        #fill both grids with empty spaces
        for row in range(9):
            for col in range(9):
                self.CURRENT_GRID[(row,col)] = " "
                self.SOLUTION_GRID[(row,col)] = " "

        #generate SOLUTION_GRID
        self.__createSolutionGrid()
        
        #use solution grid to make current grid (shows only starting nums)
        self.__createStarterGrid()

        '''
        When running the solver, it will solve the grid that is sometimes different from the solution_grid
        which means that __createStarterGrid() isn't returning only unique solutions!!!
        '''

        '''
        default_grid = [
            [" ", " ", " ", "2", "6", " ", "7", " ", "1"],
            ["6", "8", " ", " ", "7", " ", " ", "9", " "],
            ["1", "9", " ", " ", " ", "4", "5", " ", " "],
            ["8", "2", " ", "1", " ", " ", " ", "4", " "],
            [" ", " ", "4", "6", " ", "2", "9", " ", " "],
            [" ", "5", " ", " ", " ", "3", " ", "2", "8"],
            [" ", " ", "9", "3", " ", " ", " ", "7", "4"],
            [" ", "4", " ", " ", "5", " ", " ", "3", "6"],
            ["7", " ", "3", " ", "1", "8", " ", " ", " "]    ]
        '''

        #draw onto GUI
        self.__draw_grid()
        self.__draw_selectionBar()
        self.__draw_puzzle()

        #buttons
        title_font= tkFont.Font(family="Coda Caption", size=30)
        title_label = tk.Label(self.root, text="Simple\nSudoku!", height=4, width=10, font=title_font)
        title_label.pack()
        clear_button = tk.Button(self.root, text="Clear Everything", height=2, width=10, command=lambda: self.__emptyGrid())
        clear_button.pack()
        solver_button = tk.Button(self.root, text="Run Solver", height=2, width=10, command=lambda: self.__run_solver(0,0))
        solver_button.pack()
        new_puzzle_button = tk.Button(self.root, text="New Puzzle", height=2, width=10, command=lambda: self.__new_puzzle())
        new_puzzle_button.pack()
        get_hint_button = tk.Button(self.root, text="Get Hint", height=2, width=10, command= lambda: self.__get_hint())
        get_hint_button.pack()
        #pen_button = tk.Button(self.root, text="pen")
        #pen_button.pack(side=LEFT)
        #pencil_button = tk.Button(self.root, text="pencil")
        #pencil_button.pack(side=RIGHT)

        #binding
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[0], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(0))   
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[1], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(1))   
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[2], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(2))   
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[3], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(3))   
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[4], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(4))   
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[5], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(5))   
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[6], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(6))   
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[7], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(7))   
        self.canvas.tag_bind(self.SELECTION_BAR_RECTANGLES[8], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(8))  
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[0], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(0))   
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[1], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(1))   
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[2], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(2))   
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[3], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(3))   
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[4], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(4))   
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[5], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(5))   
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[6], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(6))   
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[7], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(7))   
        self.canvas.tag_bind(self.SELECTION_BAR_TEXT[8], '<ButtonPress-1>', lambda x: self.__clickedSelectionBar(8))  
        #add function so key nums change selection bar
        self.canvas.tag_bind("grid", "<Button-1>", self.__cell_clicked)
        
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

                x0 = row*self.SIDE + self.MARGIN 
                y0 = col*self.SIDE + self.MARGIN
                x1 = (row+1)*self.SIDE + self.MARGIN 
                y1 = (col+1)*self.SIDE + self.MARGIN
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tag="grid")

    def __draw_selectionBar(self):
        for row in range(9):
            x0 = row*self.SIDE + self.MARGIN 
            y0 = 0*self.SIDE + self.MARGIN + 490
            x1 = (row+1)*self.SIDE + self.MARGIN 
            y1 = (1)*self.SIDE + self.MARGIN + 490
            rectobj = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", tags="selectionBar")
            self.SELECTION_BAR_RECTANGLES.append(rectobj)
            #add text
            x = row*self.SIDE + self.MARGIN + self.SIDE / 2 
            y = 0*self.SIDE + self.MARGIN + self.SIDE / 2 + 490
            textobj = self.canvas.create_text(x, y, text=row+1, tags="selectionBar")
            self.SELECTION_BAR_TEXT.append(textobj)
            
    def __draw_puzzle(self):
        #self.canvas.delete("numbers")
        for row in range(9):
            for col in range(9):
                to_fill = self.CURRENT_GRID[(row,col)]
                x = col*self.SIDE + self.MARGIN + self.SIDE / 2
                y = row*self.SIDE + self.MARGIN + self.SIDE / 2
                box = self.canvas.create_text(x, y, text=to_fill, tags="grid")
                self.USER_VISIBLE_TEXT_OBJECTS[(row, col)] = box

    def __update_puzzle(self, row, col, newNum, color):
        self.CURRENT_GRID[(row, col)] = str(self.PEN)
        self.canvas.itemconfig(self.USER_VISIBLE_TEXT_OBJECTS[(row, col)], text=newNum, fill=color)

    def print_current_grid(self, GRID):
        for row in range(9):
            if(row % 3 == 0):
                print("-------------------------")
            print(GRID[(row,0)],GRID[(row,1)],GRID[(row,2)]," | ",
                GRID[(row,3)],GRID[(row,4)],GRID[(row,5)]," | ",
                GRID[(row,6)],GRID[(row,7)],GRID[(row,8)])
        print("-------------------------")

    #delete all numbers from 9x9 grid
    def __emptyGrid(self):
        for row in range(9):
            for col in range(9):
                if(self.canvas.itemcget(self.USER_VISIBLE_TEXT_OBJECTS[(row, col)], "fill")!="black"):
                    newString = " "
                    self.__update_puzzle(row, col, newString, "blue")
                
    # ---------------------- EVENT HANDLER METHODS ---------------------- #
    def __new_puzzle(self):
        self.__emptyGrid()
        self.__createSolutionGrid()
        self.__createStarterGrid()
        self.__draw_puzzle()

    def __get_hint(self):
        row = randrange(9)
        col = randrange(9)

        if(self.CURRENT_GRID[(row,col)].strip() == ""):
            self.__update_puzzle(row, col, self.SOLUTION_GRID[(row,col)], "purple")
        else:
            self.__get_hint()

    def __cell_clicked(self, event):
        x, y = event.x, event.y
        # get row and col numbers from x,y coordinates
        col, row = (x - self.MARGIN) / self.SIDE, (y - self.MARGIN) / self.SIDE
        self.__update_puzzle(int(row), int(col), self.PEN, "blue")

    def __clickedSelectionBar(self, num):
        #FFEB89 == light yellow
        anotherSelected = False
        for element in self.SELECTION_BAR_RECTANGLES:
            if(self.SELECTION_BAR_RECTANGLES.index(element) == num):
                pass
            elif(self.canvas.itemcget(element, "fill") == "#FFEB89"):
                anotherSelected = True
        if(anotherSelected == False):
            if(self.canvas.itemcget(self.SELECTION_BAR_RECTANGLES[num], "fill") == "#FFEB89"):
                self.canvas.itemconfig(self.SELECTION_BAR_RECTANGLES[num], fill="white")
                self.PEN = ""
            else:                
                self.canvas.itemconfig(self.SELECTION_BAR_RECTANGLES[num], fill="#FFEB89")
                self.PEN = self.canvas.itemcget(self.SELECTION_BAR_TEXT[num], "text")
    
    def __run_solver(self, masterRow, masterCol): #w/backtracking, recursion
        #base case - no more rows or columns
        if(masterRow == 8 and masterCol == 9):
            return True

        #end of row, move to next
        if(masterCol == 9):
            masterRow += 1
            masterCol = 0

        current_cell = self.canvas.itemcget(self.USER_VISIBLE_TEXT_OBJECTS[(masterRow, masterCol)], "text").strip()
        #if something already there, move on
        if(current_cell != ""):
            return self.__run_solver(masterRow, masterCol+1)

        for num in range(1,10): #try all options until one doesn't break the board
            if(self.isValid(num, masterRow, masterCol)):
                #true is safe, so fill grid space
                self.CURRENT_GRID[(masterRow,masterCol)] = str(num)
                self.canvas.itemconfig(self.USER_VISIBLE_TEXT_OBJECTS[(masterRow, masterCol)], text=str(num), fill="green")

                if(self.__run_solver(masterRow, masterCol+1)):
                    return True

                self.CURRENT_GRID[(masterRow,masterCol)] = " "
                self.canvas.itemconfig(self.USER_VISIBLE_TEXT_OBJECTS[(masterRow, masterCol)], text=" ", fill="green")
        self.print_current_grid(self.SOLUTION_GRID)
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

    def __createSolutionGrid(self):
        #self.__emptyGrid() remove anything already there
        
        #create another dictionary with options num
        options = {}
        for row in range(9):
            for col in range(9):
                options[(row,col)] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        #pick a square in the grid
        row = randrange(9)
        col = randrange(9)
        #put 1 there
        self.SOLUTION_GRID[(row, col)] = "1"
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
                    #self.__emptyGrid()
                    #self.__createSolutionGrid()
                    break
            random_box = random.choice(smallest_options)
            at_row = random_box[0]
            at_col = random_box[1]
            new_value = options[random_box[0],random_box[1]][0]
            self.SOLUTION_GRID[(at_row,at_col)] = new_value
            self.removeOptions(new_value, at_row, at_col, options)

    def __createStarterGrid(self):
        cells_not_tried = list(self.SOLUTION_GRID.keys())
        removed_counter = 0

        while(removed_counter <= 17):
            #pick a random number you haven't tried removing
            random_cell = random.choice(cells_not_tried)
            #remove the number, run your solver with the added condition that is cannot use the removed number here
            if(self.__check_removal(0,0,self.SOLUTION_GRID[(random_cell[0],random_cell[1])], random_cell[0], random_cell[1] )):
                #true -> found solution, can't remove the number
                self.CURRENT_GRID[(random_cell[0], random_cell[1])] = self.SOLUTION_GRID[(random_cell[0],random_cell[1])]
                #remove from remaining cells to drawn from
                cells_not_tried.remove(random_cell)
                removed_counter += 1
            #repeat until you have enough removed numbers (or you can't remove any more)


    def __check_removal(self, masterRow, masterCol, conditionNum, conditionRow, conditionCol): #w/backtracking, recursion
        #base case - no more rows or columns
        if(masterRow == 8 and masterCol == 9):
            return True

        #end of row, move to next
        if(masterCol == 9):
            masterRow += 1
            masterCol = 0

        current_cell = self.SOLUTION_GRID[(masterRow, masterCol)]
        #if something already there, move on
        if(current_cell != ""):
            return self.__check_removal(masterRow, masterCol+1, conditionNum, conditionRow, conditionCol)

        for num in range(1,10): #try all options until one doesn't break the board
            if(masterRow == conditionRow and masterCol == conditionCol and num == conditionNum):
                    pass
            elif(self.isValid(num, masterRow, masterCol)):
                #true is safe, so fill grid space
                self.CURRENT_GRID[(masterRow,masterCol)] = str(num)

                if(self.__check_removal(masterRow, masterCol+1, conditionNum, conditionRow, conditionCol)):
                    return True

                self.CURRENT_GRID[(masterRow,masterCol)] = " "
        return False

if __name__ == "__main__":
    root = tk.Tk(className="sudoku solver")
    my_gui = SudokuGUI(root)
    root.mainloop()
