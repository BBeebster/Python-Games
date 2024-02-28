from square import Square
import random

class Grid:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
    
    def createGrid(cols, rows):
        array = []
        for i in range(rows):
            col = []
            for j in range(cols):
                col.append(Square(False, False, False, 0))
            array.append(col)
        return array
    
    def printGrid(array):
        for row in array:
            for col in row:
                print(f"Flag is {Square.checkFlag(col)}, Mine is {Square.checkMine(col)}, nearby: {Square.checkNearby(col)}")

    def placeMines(n, array, cols, rows):
        r1 = 0
        r2 = 0
        while n > 0:
            r1 = random.randint(0, rows-1)
            r2 = random.randint(0, cols-1)
            if Square.checkMine(array[r1][r2]) is False and Square.checkKnown(array[r1][r2]) is False:
                array[r1][r2] = Square.setMine(array[r1][r2])

                if r1-1 >= 0 and r2-1 >= 0:
                    Square.upNearby(array[r1-1][r2-1])

                if r1-1 >= 0:
                    Square.upNearby(array[r1-1][r2])

                if r1-1 >= 0 and r2+1 < cols:
                    Square.upNearby(array[r1-1][r2+1])
                
                if r2-1 >= 0:
                    Square.upNearby(array[r1][r2-1])

                if r2+1 < cols:
                    Square.upNearby(array[r1][r2+1])

                if r1+1 < rows and r2-1 >= 0:
                    Square.upNearby(array[r1+1][r2-1])

                if r1+1 < rows:
                    Square.upNearby(array[r1+1][r2])

                if r1+1 < rows and r2+1 < cols:
                    Square.upNearby(array[r1+1][r2+1])

                n-=1

        return array