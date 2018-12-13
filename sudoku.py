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
import random
import itertools

__author__ = "Sam Whang | WGB"

# Error strings
array_incorrect_number_of_cells_fewer = """
Input array does not contain enough cells to fill board"""[1:]
array_incorrect_number_of_cells_greater = """
Input array contains more than number of cells on board"""[1:]

test_incorrect = [[3,0,6,5,0,8,4,9,9],
                  [5,2,0,0,0,0,0,0,0],
                  [0,8,7,0,0,0,0,3,1],
                  [0,0,3,0,1,0,0,8,0],
                  [9,0,0,8,6,3,0,0,5],
                  [0,5,0,0,9,0,6,0,0],
                  [1,3,0,0,0,0,2,5,0],
                  [0,0,0,0,0,0,0,7,4],
                  [0,0,5,2,0,6,3,0,0]]

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

test_example = [[0,6,7,0,9,0,0,2,3],
                [0,9,0,5,0,6,0,0,0],
                [0,8,0,4,0,0,0,0,0],
                [9,2,0,0,0,0,0,0,0],
                [7,0,0,1,6,0,0,0,0],
                [0,0,0,0,0,0,7,6,0],
                [0,0,2,0,0,0,0,1,0],
                [0,4,3,0,0,0,9,0,6],
                [0,0,0,7,4,0,0,3,8]]

def matrix_to_list(matrix):
    return itertools.chain.from_iterable(matrix)

def string_2_list(string):
    return string.split()

index_counter = lambda i, j: i * 9 + j
block_counter = lambda r, c: r // 3 * 3 + c // 3

def flatten(array):
    """Converts a list of lists into a single list of x elements"""
    return [x for row in array for x in row]

def shuffle(s: set) -> list:
    """
    Transforms the set into a list randomly shuffled
    """
    s = list(s)
    random.shuffle(s)
    return s

def shuffle_pop(s: set) -> int:
    """After shuffling the input set, returns one value from the set"""
    s = shuffle(s)
    try:
        return s.pop()
    except IndexError:
        return 0

def remaining_cells(board: list):
    """
    Iterates through a board represented by a 1D list and retrieves the
    row, column, block and index number for each position in the grid
    that does not hold a valid value ie. 0
    """
    q = []
    for row in range(9):
        for col in range(9):
            index = index_counter(row, col)
            if board[index] == 0:
                block = block_counter(row, col)
                row.append((row, col, block, index))
        q += row if i % 2 == 0 else row[::-1]
    return q

def all_cells():
    """
    Retrieves the row, column, block and index number for each value on a
    board represented by a 1D list
    """
    q = [] # holds the indices in the order they will be accessed.
    for r in range(9):
        row = []
        for c in range(9):
            b = block_counter(r, c)
            index = index_counter(i, j)
            row.append((r, c, b, index))
        q += row if i % 2 == 0 else row[::-1]
    return q

def format_col(col: list) -> str:
    """
    Transforms [1,2,3] -> 1,
                          2,
                          3
    """
    return "\n".join(str(i) for i in col)

def format_row(row):
    """
    Transforms [1, 2, 3] -> 1 2 3
    """
    return " ".join(str(i) for i in row)

def format_block(block: list) -> str:
    """
    Transforms [1, 2, 3, 4, 5, 6, 7, 8] -> 1 2 3
                                           4 5 6
                                           7 8 9
    """
    return "\n".join(" ".join(str(v) for v in block[i*3:i*3+3]) 
                                        for i in range(3))

def parse_int_input(s: str) -> list:
    """
    Transforms '12345' -> [1, 2, 3, 4, 5]
    Raises errors on invalid input. Ex: '12a45' -> Error
    """
    try:
        row = [int(v) for v in s]
        return row
    except:
        raise

def input_rows() -> list:
    """
    Asks for user input on every row
    Row 1: '...'
    ...
    Row 9: '...'
    """
    return [parse_input(input(f"Row {r + 1}: ")) for r in range(9)]

def input_single() -> list:
    """
    Asks for user input on every value in grid
    Board: '...' WHERE len('...') == 81
    """
    string = input("Board: ")
    if len(string) != 81:
        raise ValueError("input_single(): Invalid input")
    strings = split_rows(string)
    return parse_rows(strings)

def split_rows(array:list, l:int=9) -> list:
    """
    Transforms a 1D list into a list of lists with every list holding l 
    elements. Error is raised if array has a length not divisible by l.
    """
    if len(array) % l != 0:
        raise ValueError("split_rows(): Rows in list have different lengths")
    return [array[i:i+l] for i in range(0, len(array), l)]

def parse_rows(array: list) -> list:
    """
    Transforms the element types within a list of lists from string to integer
    """
    return [parse_int_input(row) for row in array]

# TODO: possibly subclass some class functions to other classes
#       for now go ahead with the assumption of a 2D matrix
#       The simplest implementation would be using a 1D list to
#       represent the board with index methods to retrieve the
#       correct cells within the list.
# EDIT: List grid implements a 1D list.
class ListGrid:
    """Holds a list that represents the board"""
    def __init__(self, grid: list=None, build: bool=True) -> None:
        """
        If no grid is given, will build a new list. If board is not valid
        on init, then the board will be filled until it is valid or an error
        is thrown.
        """
        self.grid = grid
        empty = False
        if not self.grid:
            empty = True
            self.grid = [0 for _ in range(81)]
        if not self.valid_board and build:
            self.cells = all_cells() if empty else remaining_cells(self.grid)
            if not self.build_board() and not empty:
                raise ValueError("Given board was incorrect")

    def __str__(self):
        return self.board
    
    def __repr__(self):
        return self.board

    def __eq__(self, other):
        return self.grid == other.grid

    def __hash__(self):
        rows = split_rows(self.grid)
        h = []
        for row in rows:
            h.append(hash(''.join(map(str, row))))
        return hash(''.join(map(str, h)))

    def build_board(self) -> None:
        """Used to fill values on an empty board"""
        if (self.valid_board):
            return True

        cell = self.cells.pop(0)
        i = cell[3]
        vals = self.possible_values(cell)

        for v in shuffle(vals):
            self.grid[i] = v

            if self.build_board():
                return True

            self.grid[i] = 0

        # no values fit. Put the cell back and try again.
        self.cells.insert(0, cell)
        return False

    @property
    def board(self):
        """Allows access of board representation as a string property"""
        divider = "-" * 25
        b = [divider]
        for i in range(9):
            r = []
            for j in range(3):
                s = index_counter(i, j * 3)
                e = s + 3
                r.append(' '.join(str(i) for i in self.grid[s:e]))
            b.append(f"| {r[0]} | {r[1]} | {r[2]} |")
            if (i + 1) % 3 == 0:
                b.append(divider)
        return "\n".join(b)

    def print_board(self, current_board: list=None) -> None:
        """Outputs the grid to terminal with formatting"""
        b = current_board
        if not current_board:
            b = self.grid
        divider = "-" * 25
        print(divider)
        for i in range(9):
            r = []
            for j in range(3):
                s = index_counter(i, j * 3)
                e = s + 3
                r.append(' '.join(str(i) for i in b[s:e]))
            print(f"| {r[0]} | {r[1]} | {r[2]} |")
            if (i + 1) % 3 == 0:
                print(divider)

    def check_range(self, value: int) -> bool:
        """Returns a value indicating if value is within length of board"""
        return 0 <= value < 9

    def check_grid(self) -> None:
        """Returns a value indicating if board has number of correct cells"""
        if not len(self.grid) == 81:
            raise ValueError("Grid does not have 81 elements. Aborting")

    def possible_values(self, cell):
        """
        Returns values not located in the row, column, or block for input
        cell index.
        """
        r, c, b, _ = cell
        vals = set(j + 1 for j in range(9))
        vals -= set(self.row(r))
        vals -= set(self.col(c))
        vals -= set(self.block(b))
        vals -= {0}
        return vals

    @property
    def valid_board(self):
        """Determines if the board is in a valid state"""
        self.check_grid()
        r = self.all_rows_valid()
        c = self.all_cols_valid()
        b = self.all_blocks_valid()
        return r and c and b

    def row(self, rownum: int) -> list:
        """Returns the values of row with the given row number"""
        self.check_grid()
        if not self.check_range(rownum):
            raise ValueError(f"Row {rownum} is not in range(0, 8)")
        index_start = rownum * 9
        return self.grid[index_start:index_start+9]

    def row_valid(self, rownum: int) -> bool:
        """Returns a value indicating the given row is valid"""
        row = self.row(rownum)
        return len(row) == 9 == len(set(row) - {0})

    def rows_valid(self) -> list:
        """Returns a list with values indicating validness for each row"""
        return list(self.row_valid(row) for row in range(9))

    def all_rows_valid(self) -> bool:
        """Returns a value indicating if all rows are valid"""
        return all(self.rows_valid())

    def col(self, colnum: int) -> list:
        """
        Returns a column from the 1d grid corresponding to the column number
        passed in.
        """
        if not self.check_range(colnum):
            raise ValueError(f"Col {colnum} is not in range(0, 8)")
        return self.grid[colnum::9]

    def col_valid(self, colnum: int) -> bool:
        """
        Returns a value indicating whether the pulled column fits the 
        constraints of a valid column.
        """
        col = self.col(colnum)
        return len(col) == 9 == len(set(col) - {0})

    def cols_valid(self) -> list:
        """Returns the values of all columns indicating validness"""
        return list(self.col_valid(col) for col in range(9))

    def all_cols_valid(self) -> bool:
        """Returns a value indicating all columns in the grid are valid"""
        return all(self.cols_valid())

    def block(self, blocknum: int) -> list:
        """
        Returns a block as a 1d array from the 1d grid corresponding to the
        block number passed in as a parameter
        """
        if not self.check_range(blocknum):
            raise ValueError(f"Block {blocknum} is not in range(0, 8)")
        block = []
        for j in range(3):
            index = blocknum * 3 + j * 9 + 18 * (blocknum // 3)
            for val in self.grid[index:index+3]:
                block.append(val)
        return block

    def block_valid(self, blocknum: int) -> bool:
        """
        Returns a value indicating whether the pulled block fits the 
        constraints of a valid block
        """
        blk = self.block(blocknum)
        return len(blk) == 9 == len(set(blk) - {0})

    def blocks_valid(self) -> list:
        """
        Returns a value for each block in the grid determining each individual
        block validness
        """
        return list(self.block_valid(block) for block in range(9))

    def all_blocks_valid(self) -> bool:
        """
        Returns a value indicating if all blocks in the grid are valid
        """
        return all(self.blocks_valid())

    @classmethod
    def from_input_rows_manual(cls) -> object:
        """Builds a new ListGrid from valid user input"""
        return cls(input_rows())

    @classmethod
    def from_input_once_single(cls) -> object:
        """Builds a new ListGrid from valid user input"""
        return cls(input_single())
    
    @classmethod
    def from_input_once_multiple_rows(cls) -> object:
        """Builds a new ListGrid from valid user input"""
        return cls(input_multiple())

    @classmethod
    def from_matrix(cls, matrix: list) -> object:
        """Builds a new ListGrid with a given 2d matrix"""
        return cls(list(matrix_to_list(matrix)))

    @classmethod
    def init_complete(cls) -> object:
        """
        Builds a new ListGrid with a complete grid passed in. Used to test
        the ListGrid."""
        return cls.from_matrix(test_complete)

    @classmethod
    def init_incomplete(cls) -> object:
        """
        Builds a new ListGrid with an incomplete grid passed in. Used to test
        the ListGrid.
        """
        return cls.from_matrix(test_incomplete)

    @classmethod
    def init_incorrect(cls) -> object:
        """
        Builds a new ListGrid with a grid that is impossible to complete. Used
        to test the ListGrid."""
        return cls.from_matrix(test_incorrect)

class Cell:
    """Object to hold the value player places in the given position"""
    def __init__(self, pos, value):
        self.position = index
        self.value_current, self.value_correct = value
        if self.value_current == 0:
            self.removable = True

    @property
    def empty(self):
        return self.value != 0

    @property
    def value(self):
        return self.value_current

    @value.setter
    def value(self, val):
        self.value_current = val

    @property
    def correct(self):
        return self.value_correct == self.value_current
    
    @property
    def string_grid(self):
        return self.value_current

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

class UIBoard:
    """
    The UI class representing the board.
    """
    def __init__(self, grid):
        self.data = ListGrid(grid)

class MatrixGrid:
    """Holds 9 blocks and grid functions to determine if all 
    nine blocks are valid
    """
    def __init__(self, grid: list=None, build: bool=True) -> None:
        """
        If no grid is given, will build a new list. If board is not valid
        on init, then the board will be filled until it is valid or an error
        is thrown.
        """
        self.grid = grid
        empty = False
        if not self.grid:
            empty = True
            self.grid = [0 for _ in range(81)]
        if not self.valid_board and build:
            if empty:
                self.cells = all_cells()
            else:
                predicate = check_map_1d_position_empty
                self.cells = remaining_cells(self.grid, predicate)
            if not self.build_board() and not empty:
                raise ValueError("Given board was incorrect")

    @property
    def valid_board(self):
        """Determines if the board is in a valid state"""
        self.check_grid()
        r = self.all_rows_valid()
        c = self.all_cols_valid()
        b = self.all_blocks_valid()
        return r and c and b

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

    def all_blocks_valid(self):
        pass

    def block_valid(self):
        pass

    def row_valid(self):
        pass

    def col_valid(self):
        pass

if __name__ == "__main__":
    reference = False
    if reference:
        lines = [
            bot, box, top, box, top, box, div, box, top, box, top, 
            box, div, box, top, box, top, box, bot, ovr, num, top
        ]

        for line in lines:
            print(line)

    l = ListGrid.init_complete()
    print(l)
    l = ListGrid.init_incomplete()
    print(l)