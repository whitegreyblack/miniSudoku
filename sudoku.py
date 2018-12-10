"""
Sudoku app using curses to create the board

Could number all boards from 0->80 or 1->81.
- OR -
Could use nested dictionaries to represent the grid:
    {
        (0, 0): 
        {
            (0->3, 0->3, y*3+x): val,
            ...
        },
        ...
        (2, 2): ...
    }
"""

import pprint
import itertools

__author__ = "Sam Whang | WGB"

array_incorrect_number_of_cells_fewer = """
Input array does not contain enough cells to fill board"""[1:]
array_incorrect_number_of_cells_greater = """
Input array contains more than number of cells on board"""[1:]
test_incomplete = [[3,0,6,5,0,8,4,0,0],
                   [5,2,0,0,0,0,0,0,0],
                   [0,8,7,0,0,0,0,3,1],
                   [0,0,3,0,1,0,0,8,0],
                   [9,0,0,8,6,3,0,0,5],
                   [0,5,0,0,9,0,6,0,0],
                   [1,3,0,0,0,0,2,5,0],
                   [0,0,0,0,0,0,0,7,4],
                   [0,0,5,2,0,6,3,0,0]]

test_complete = [[3,6,9,1,2,4,5,8,7],
                 [7,2,8,6,5,9,3,1,4],
                 [1,4,5,7,3,8,2,6,9],
                 [2,9,7,3,6,1,8,4,5],
                 [5,8,3,9,4,2,6,7,1],
                 [6,1,4,5,8,7,9,2,3],
                 [9,7,2,8,1,5,4,3,6],
                 [4,5,6,2,7,3,1,9,8],
                 [8,3,1,4,9,6,7,5,2]]

def matrix_to_list(matrix):
    return itertools.chain.from_iterable(matrix)

def string_2_list(string):
    return string.split()

class Cell:
    """Object to hold the value player places in the given position"""
    def __init__(self, row, col, box):
        self.pos = (row, col, box)
        self.val = None
    def empty():
        return self.val is 0 or self.val is None

class Block:
    """
    Holds 9 cells and functions to determine if all nine
    cells are valid
    """
    def __init__(self, row, col):
        self.pos = (row, col)
        self.cells = {
            (i, j): Cell(i, j, self.pos[1] * 3 + self.pos[0]) 
                for i in range(3)
                    for j in range(3)
        }

# TODO: possibly subclass some class functions to other classes
#       for now go ahead with the assumption of a 2D matrix
#       The simplest implementation would be using a 1D list to
#       represent the board with index methods to retrieve the
#       correct cells within the list.
class ListGrid:
    """Holds a list that represents the board"""
    def __init__(self, grid: list=None):
        self.grid = grid
    def build_board(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
    def check_range(self, value: int) -> bool:
        return 0 <= value < 9
    def check_grid(self) -> None:
        if not len(self.grid) == 81:
            raise ValueError("Grid does not have 81 elements. Aborting")
    def row(self, rownum: int) -> list:
        self.check_grid()
        if not self.check_range(rownum):
            raise ValueError(f"Row {rownum} is not in range(0, 8)")
        index_start = rownum * 9
        return self.grid[index_start:index_start+9]
    def row_valid(self, rownum: int) -> bool:
        row = self.row(rownum)
        return len(row) == 9 and len(row) == len(set(row))
    def rows_valid(self) -> list:
        return list(self.row_valid(row) for row in range(9))
    def all_rows_valid(self) -> bool:
        return all(self.rows_valid())
    def col(self, colnum: int) -> list:
        if not self.check_range(colnum):
            raise ValueError(f"Col {colnum} is not in range(0, 8)")
        index_start = colnum
        return self.grid[index_start::9]
    def col_valid(self, colnum: int):
        col = self.col(colnum)
        return len(col) == 9 and len(col) == len(set(col))
    def cols_valid(self) -> list:
        return list(self.col_valid(col) for col in range(9))
    def all_cols_valid(self) -> bool:
        return all(self.cols_valid())
    def block(self, blocknum: int) -> list:
        if not self.check_range(blocknum):
            raise ValueError(f"Block {blocknum} is not in range(0, 8)")
        block = []
        for j in range(3):
            index=blocknum * 3 + j * 9 + 18 * (blocknum // 3)
            for val in self.grid[index:index+3]:
                block.append(val)
        return block
    def blocks_valid(self) -> list:
        return list(self.block_valid(block) for block in range(9))
    def all_blocks_valid(self) -> bool:
        return all(self.blocks_valid())
    @classmethod
    def from_matrix(cls, matrix: list) -> object:
        return cls(list(matrix_to_list(matrix)))
    @classmethod
    def init_empty(cls) -> object:
        return cls(list())
    @classmethod
    def init_complete(cls) -> object:
        return cls.from_matrix(test_complete)
    @classmethod
    def init_incomplete(cls) -> object:
        return cls.from_matrix(test_incomplete)


class Grid:
    """Holds 9 blocks and grid functions to determine if all 
    nine blocks are valid
    """
    def __init__(self, grid=None):
        self.grid = grid
        # if no grid then use test case
        if not self.grid:
            self.grid = test_grid
        self.blocks = {(i, j): Block(i, j) for i in range(3) for j in range(3)}
    def __repr__(self):
        return str(self.grid)
    def draw(self):
        pprint.pprint(self.grid)
    @classmethod
    def from_array(self, array):
        if len(array) != 81:
            if len(array) < 81:
                raise ValueError(array_incorrect_number_of_cells_fewer)
            raise ValueError(array_incorrect_number_of_cells_greater)
        return Grid([array[w:w+9] for w in range(0, len(array), 9)])
    def to_matrix(self):
        return
    @classmethod
    def from_json(self, dictionary):
        return Grid()
    def to_json(self):
        """
        With json, the board can be represented with all filled/given cells as
        a position index with value and any positions not in the given data
        considered as unfilled
        """
        return
    def block_valid(self):
        pass
    def row_valid(self):
        pass
    def col_valid(self):
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
