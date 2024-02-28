import tkinter as tk
import time
from grid import Grid
from square import Square

rows = 20
cols = 40
ht = 600
wd = 1200

mines = 100
flags = 0
start = False

dead = False
#generate the grid data
field = Grid.createGrid(cols, rows)
Grid.placeMines(mines, field, cols, rows)

#create window
root = tk.Tk()
root.title("pySweeper")

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
                widget[0].destroy()
                #set the known state to true
                Square.setKnown(field[r+dr][c+dc])
                #if the nearby square is also a 0 square, then call the function again
                if Square.checkNearby(field[r+dr][c+dc]) == 0:
                    remove_nearby (r+dr, c+dc)

#define action of left click
def left_click(event):
    global dead
    if dead is False:
        #get location of the square
        x = event.x_root - root.winfo_rootx()
        y = event.y_root - root.winfo_rooty()
        c = int(((x)/wd*cols))
        r = int(((y)/ht*rows))
        if Square.checkFlag(field[r][c]) is False:
            #see if there is a mine at the positon
            if (Square.checkMine(field[r][c])) is True:
                event.widget.destroy()
                print(f"{Square.checkMine(field[r][c])}game over")
                dead = True

            else:
                Square.setKnown(field[r][c])
                #if the space is a 0 destroy all nearby squares
                if (Square.checkNearby(field[r][c])) == 0:
                    remove_nearby(r, c)
                #destroy the square clicked on
                event.widget.destroy()

#define action of right click
def right_click(event):
    global dead
    #get location of the square
    x = event.x_root - root.winfo_rootx()
    y = event.y_root - root.winfo_rooty()
    c = int(((x)/wd*cols))
    r = int(((y)/ht*rows))

    #check flage state and update accordingly
    if (Square.checkFlag(field[r][c])) is True and dead is False:
        event.widget.configure(bg="black")
    elif dead is False:
        event.widget.configure(bg="red")

    #update flag state
    Square.setFlag(field[r][c])

#display lower frames
for i in range(rows):
    for j in range(cols):
        #hidden frames displaying state of square
        hidden = tk.LabelFrame(root, width=wd/cols, height=ht/rows).grid(column=j, row=i)
        if (Square.checkMine(field[i][j])) is True:
            mine = tk.Label(hidden, text = f"{Square.checkMine(field[i][j])}").grid(column=j, row=i)
        else: 
            if (Square.checkNearby(field[i][j])) == 0:
                nearby = tk.Label(hidden, text = f"").grid(column=j, row=i)
            else: 
                nearby = tk.Label(hidden, text = f"{Square.checkNearby(field[i][j])}").grid(column=j, row=i)

#display upper frames
for i in range(rows):
    for j in range(cols):
        #frames displaying cover for hidden state of squares
        cover = tk.Frame(root, width=wd/cols, height=ht/rows, background="black")
        cover.grid(column=j,row=i)

        #bind cover frame to buttons
        cover.bind("<Button-1>", left_click)
        cover.bind("<Button-2>", right_click)
        cover.bind("<Button-3>", right_click)

root.mainloop()
