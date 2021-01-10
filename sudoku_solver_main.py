#Sudoku Solver
import tkinter as tk
from random import randrange
import random


class SudokuGUI:
    
    

    def __init__(self, root):
        #instance vars
        self.root = root #Tk Window
        self.solutionGrid = {}
        self.pen = ""

        root.geometry("600x700") #set width x height
        root.configure(bg="white")

        #make header
        self.header_frame = tk.Frame(root)
        self.title_label = tk.Label(self.header_frame, text="Sudoku Solver", bg="white")
        self.title_label.config(font=("Consolas",30))
        self.title_label.pack()
        self.header_frame.pack(pady=30)

        #create selection bar w/1-9 options
        self.selectionBar_frame = tk.Frame(root)
        
        boxOne = tk.Label(self.selectionBar_frame, text="1", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxTwo = tk.Label(self.selectionBar_frame, text="2", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxThree = tk.Label(self.selectionBar_frame, text="3", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxFour = tk.Label(self.selectionBar_frame, text="4", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxFive = tk.Label(self.selectionBar_frame, text="5", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxSix = tk.Label(self.selectionBar_frame, text="6", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxSeven = tk.Label(self.selectionBar_frame, text="7", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxEight = tk.Label(self.selectionBar_frame, text="8", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxNine = tk.Label(self.selectionBar_frame, text="9", bg="#e6e6e6", borderwidth=2, relief="groove", width=4, height=2)
        boxOne.grid(row=0, column=0)
        boxTwo.grid(row=0, column=1)
        boxThree.grid(row=0, column=2)
        boxFour.grid(row=0, column=3)
        boxFive.grid(row=0, column=4)
        boxSix.grid(row=0, column=5)
        boxSeven.grid(row=0, column=6)
        boxEight.grid(row=0, column=7)
        boxNine.grid(row=0, column=8)
        selectionBar = [boxOne, boxTwo, boxThree, boxFour, boxFive, boxSix, boxSeven, boxEight, boxNine]

        boxOne.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxOne, selectionBar))
        boxTwo.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxTwo, selectionBar))
        boxThree.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxThree, selectionBar))
        boxFour.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxFour, selectionBar))
        boxFive.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxFive, selectionBar))
        boxSix.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxSix, selectionBar))
        boxSeven.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxSeven, selectionBar))
        boxEight.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxEight, selectionBar))
        boxNine.bind("<Button-1>", lambda box_label: self.clickedSelectionBar(boxNine, selectionBar))

        self.selectionBar_frame.pack(padx=5)
        
        #create a blank 9x9 grid
        self.frame = tk.Frame()
        boxes = {}
        for row in range(9):
            for col in range(9):
                if(row in (0,1,2,6,7,8) and col in (3,4,5)):
                    color="#b3d9ff" #light blue
                elif(row in (3,4,5) and col in (0,1,2,6,7,8)):
                    color="#b3d9ff" #light blue
                else:
                    color="#e6e6e6" #grey
                self.box = tk.Label(self.frame, text="", bg=color, borderwidth=2, relief="groove", width=4, height=2)
                self.box.grid(row=row+1, column=col)
                boxes[(row, col)] = self.box #this way can edit each box later
        self.frame.pack(padx=5, pady=50)

        #Add Buttons
        self.fill_button = tk.Button(root, text="Fill",command= lambda: self.fillSolutionGrid(boxes), highlightbackground="white")
        self.fill_button.pack()
        self.solve_button = tk.Button(root, text="Solve",command=self.solve, highlightbackground="white")
        self.solve_button.pack()
        self.clear_button = tk.Button(root, text="Clear",command=lambda: self.emptyGrid(boxes), highlightbackground="white")
        self.clear_button.pack()

    #fill board
    def fillSolutionGrid(self, grid={}):
        self.emptyGrid(grid) #remove anything already there
        
        #create another dictionary with options num
        options = {}
        for row in range(9):
            for col in range(9):
                options[(row,col)] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        #pick a random square in the grid
        row = randrange(9)
        col = randrange(9)
        selected = grid[(row, col)]
        #put 1 there
        selected.configure(text="1")
        self.removeOptions("1", row, col, options) #delete 1 from invalid places

        while(self.isFull(grid) is False):
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
                if(self.isFull(grid) is False):
                    self.emptyGrid(grid)
                    self.fillSolutionGrid(grid)
                    break
            random_box = random.choice(smallest_options)
            at_row = random_box[0]
            at_col = random_box[1]
            new_value = options[random_box[0],random_box[1]][0]
            grid[(at_row,at_col)].configure(text=new_value)
            self.removeOptions(new_value, at_row, at_col, options)
        self.solutionGrid = grid

    #to remove numbers:
        #pick a random number you haven't tried removing
        #remove the number, run your solver with the added condition that is cannot use the removed number here
        #if the solver finds a solution, you can't remove the number
        #repeat until you have enough removed numbers (or you can't remove any more)

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


    ####################################################
                        

    #is the 9x9 grid full?
    def isFull(self, grid={}):
        for row in range(9):
            for col in range(9):
                if(grid[(row,col)].cget("text").strip() == ""):
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
    def emptyGrid(self, grid = {}):
        for row in range(9):
            for col in range(9):
                grid[(row,col)].configure(text="")

    # ---------------------- EVENT HANDLER METHODS ---------------------- #
    def clickedSelectionBar(self, label, selectionBar):
        #FFEB89 == yellow
        anotherSelected = False
        for element in selectionBar:
            #print(element.cget("bg"))
            if(element == label):
                pass
            elif(element.cget("bg") == "#FFEB89"):
                anotherSelected = True
        if(anotherSelected == False):
            if(label.cget("bg") == "#FFEB89"):
                label.configure(bg="#e6e6e6")
                self.pen = ""
            else:
                label.configure(bg="#FFEB89")
                self.pen = label.cget("text")            
    



if __name__ == "__main__":
    root = tk.Tk(className="sudoku solver")
    my_gui = SudokuGUI(root)
    root.mainloop()
