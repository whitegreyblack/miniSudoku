# Sudoku app using curses to create the board
import pprint

__author__ = "Sam Whang | WGB"

class Cell:
    def __init__(self, row, col, box):
        self.pos = (row, col, box)
        self.val = None
    def empty():
        return self.val is 0 or self.val is None

class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.grid=[[3,0,6,5,0,8,4,0,0],
		   [5,2,0,0,0,0,0,0,0],
		   [0,8,7,0,0,0,0,3,1],
		   [0,0,3,0,1,0,0,8,0],
		   [9,0,0,8,6,3,0,0,5],
		   [0,5,0,0,9,0,6,0,0],
		   [1,3,0,0,0,0,2,5,0],
		   [0,0,0,0,0,0,0,7,4],
		   [0,0,5,2,0,6,3,0,0]] 
    def fill(self):
        pass
    def draw(self):
        pprint.pprint(self.grid)
    def solve(self):
        pass 

if __name__ == "__main__":
    top="#---+---+---#---+---+---#---+---+---#"
    div="############@###########@############"
    box="#   |   |   #   |   |   #   |   |   #"
    bot="#####################################"
    ovr="+---+---+---+---+---+---+---+---+---+"
    num="| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |"
    und="+---+---+---+---+---+---+---+---+---+"
    print(bot)
    print(box)
    print(top)
    print(box)
    print(top)
    print(box)
    print(div)
    print(box)
    print(top)
    print(box)
    print(top)
    print(box)
    print(div)
    print(box)
    print(top)
    print(box)
    print(top)
    print(box)
    print(bot)
    print(ovr)
    print(num)
    print(top)
    print(len(top))
    print(33-12)

    grid = Grid()
    grid.draw()
