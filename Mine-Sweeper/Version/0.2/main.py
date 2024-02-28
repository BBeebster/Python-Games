import tkinter as tk
from grid import Grid
from square import Square

rows = 20
cols = 20
ht = 600
wd = 600

mines = 100
flags = 0

#use this boolean to determine a first click
start = False

dead = False


#create an empty grid
field = Grid.createGrid(cols, rows)

#create window
root = tk.Tk()
root.title("pySweeper")

def set_nearby_known(r, c):
    #going to set some parameters to iterate through other squares
    r1,r2,c1,c2 = -1, 2, -1, 2

    #reset parameters if square is on an edge
    if r == 0:
        r1 = 0
    if r == rows-1:
        r2 = 1
    if c == 0:
        c1 = 0
    if c == cols-1:
        c2 = 1

    #now we go through the nearby mines
    for dr in range (r1, r2):
        for dc in range (c1, c2):
            #make sure the square is not known before we update it to prevent bugs
            if Square.checkKnown(field[r+dr][c+dc]) is False:
                Square.setKnown(field[r+dr][c+dc])

def set_nearby_unknown(r, c):
    #going to set some parameters to iterate through other squares
    r1,r2,c1,c2 = -1, 2, -1, 2

    #reset parameters if square is on an edge
    if r == 0:
        r1 = 0
    if r == rows-1:
        r2 = 1
    if c == 0:
        c1 = 0
    if c == cols-1:
        c2 = 1

    #now we go through the nearby mines
    for dr in range (r1, r2):
        for dc in range (c1, c2):
            #make sure the square is not known before we update it to prevent bugs
            if Square.checkKnown(field[r+dr][c+dc]) is True:
                Square.setUnknown(field[r+dr][c+dc])

#this is a recursive function to remove nearby squares to the one clicked on
def remove_nearby(r, c):
    #going to set some parameters to iterate through other squares
    r1,r2,c1,c2 = -1, 2, -1, 2

    #reset parameters if square is on an edge
    if r == 0:
        r1 = 0
    if r == rows-1:
        r2 = 1
    if c == 0:
        c1 = 0
    if c == cols-1:
        c2 = 1

    #now we go through the nearby mines
    for dr in range (r1, r2):
        for dc in range (c1, c2):
            #make sure the square is not known before we update it to prevent bugs
            if Square.checkKnown(field[r+dr][c+dc]) is False:
                #destroy the cover frame
                widget = root.grid_slaves(row = r+dr, column = c+dc)

                #set the known state to true
                Square.setKnown(field[r+dr][c+dc])

                if Square.checkNearby(field[r+dr][c+dc]) != 0:
                    if Square.checkMine(field[r+dr][c+dc]) is False:
                        widget[0].configure(bg="white")
                        label = tk.Label(widget[0], text =f"{Square.checkNearby(field[r+dr][c+dc])}").pack()
                #if the nearby square is also a 0 square, then call the function again
                if Square.checkNearby(field[r+dr][c+dc]) == 0:
                    remove_nearby (r+dr, c+dc)
                    widget[0].configure(bg="white")

#define action of left click
def left_click(event):
    global start
    global field
    global dead
    if dead is False:
        #get location of the square
        x = event.x_root - root.winfo_rootx()
        y = event.y_root - root.winfo_rooty()
        c = int(((x)/wd*cols))
        r = int(((y)/ht*rows))
        if start is False:
            Square.setKnown(field[r][c])
            set_nearby_known(r,c)
            Grid.placeMines(mines, field, cols, rows)
            set_nearby_unknown(r,c)
            if (Square.checkNearby(field[r][c])) == 0:
                event.widget.configure(bg="white")
                remove_nearby(r, c)
            else:
                event.widget.configure(bg="white")
                label = tk.Label(event.widget, text =f"{Square.checkNearby(field[r][c])}").pack()
                remove_nearby(r, c)
            
            start = True
        else:
            if Square.checkFlag(field[r][c]) is False:
                #see if there is a mine at the positon
                if (Square.checkMine(field[r][c])) is True:
                    event.widget.configure(bg="white")
                    label = tk.Label(event.widget, text ="M").pack()
                    print(f"{Square.checkMine(field[r][c])}game over")
                    dead = True

                else:
                    Square.setKnown(field[r][c])
                    #if the space is a 0 destroy all nearby squares
                    if (Square.checkNearby(field[r][c])) == 0:
                        remove_nearby(r, c)
                        event.widget.configure(bg="white")
                    else:
                        #destroy the square clicked on
                        event.widget.configure(bg="white")
                        label = tk.Label(event.widget, text =f"{Square.checkNearby(field[r][c])}").pack()

#define action of right click
def right_click(event):
    global dead
    global flags
    #get location of the square
    x = event.x_root - root.winfo_rootx()
    y = event.y_root - root.winfo_rooty()
    c = int(((x)/wd*cols))
    r = int(((y)/ht*rows))

    #check flage state and update accordingly
    if (Square.checkFlag(field[r][c])) is True and dead is False:
        event.widget.configure(bg="black")
        flags -= 1
    elif dead is False and flags < mines:
        event.widget.configure(bg="red")
        flags += 1

    #update flag state
    Square.setFlag(field[r][c])

#display upper frames
for i in range(rows):
    for j in range(cols):
        #frames displaying cover for hidden state of squares
        cover = tk.LabelFrame(root, width=wd/cols, height=ht/rows, background="black")
        cover.grid(column=j,row=i)

        #bind cover frame to buttons
        cover.bind("<Button-1>", left_click)
        cover.bind("<Button-2>", right_click)
        cover.bind("<Button-3>", right_click)

#give values to the hidden frame on first click of an upper frame


root.mainloop()