"""
tool.py
Holds resources and functions used in other files
"""
import random
import itertools
import functools

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

def list_to_str(l: list, delim: str=""):
    return hash(delim.join(map(str, l)))

def matrix_to_array(matrix):
    return list(itertools.chain.from_iterable(matrix))

def array_to_matrix(array):
    pass

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

def print_board(current_board: list=None) -> None:
    """Outputs the grid to terminal with formatting"""
    b = current_board
    divider = "-" * 25
    print(divider)
    for i in range(9):
        r = []
        for j in range(3):
            s = index_counter(i, j * 3)
            r.append(' '.join(str(i) for i in b[s:e+3]))
        print(f"| {r[0]} | {r[1]} | {r[2]} |")
        if (i + 1) % 3 == 0:
            print(divider)

def remaining_cells(board: list):
    """
    Iterates through a board represented by a 1D list and retrieves the
    row, column, block and index number for each position in the grid
    that does not hold a valid value ie. 0
    """
    q = []
    for r in range(9):
        row = []
        for c in range(9):
            index = index_counter(r, c)
            if board[index] == 0:
                block = block_counter(r, c)
                row.append((r, c, block, index))
        q += row if r % 2 == 0 else row[::-1]
    return q

def remaining_cells_2d(board: list):
    """
    Iterates through a board represented by a 1D list and retrieves the
    row, column, block and index number for each position in the grid
    that does not hold a valid value ie. 0
    """
    q = []
    for r in range(9):
        row = []
        for c in range(9):
            if board[r][c] == 0:
                block = block_counter(r, c)
                row.append((r, c, block, index))
        q += row if r % 2 == 0 else row[::-1]
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
            index = index_counter(r, c)
            row.append((r, c, b, index))
        q += row if r % 2 == 0 else row[::-1]
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

def limit_param_range(func):
    print('a', func)
    functools.wraps(func)
    def wrapper_limit(arg):
        print('b', arg)
        for a in arg[1]:
            if not 0 <= arg[1] < 9:
                raise ValueError("""
Function paramater out of range. Expected: 0-8. Got: {arg}"""[1:])
        return func(arg)
    return wrapper_limit

