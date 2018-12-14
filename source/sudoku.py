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
from listgrid import ListGrid
from matrixgrid import MatrixGrid

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

class UIGrid(ListGrid):
    @property
    def board(self):
        """View aka the front end."""
        grid = ["=" * 55]
        for row in range(27):
            colstr = []
            for col in range(9):
                scol = []
                for subcol in range(3):
                    index = row // 3 * 9 + col
                    subindex = row * 27 + col * 3 + subcol
                    value = self.cell(index)
                    block = row // 3 + subcol
                    scol.append(str(value) if value == block else ' ')
                colstr.append('|' + ''.join(scol) + '|')
            grid.append('|' + '|'.join(colstr) + '|')
            if (row + 1) % 9 == 0:
                grid.append("=" * 55)
            elif (row + 1) % 3 == 0:
                grid.append("-" * 55)
        return '\n'.join(grid)
    @property
    def index(self):
        return self._i
    @property
    def index(self):
        temp = self._i
        self._i += i
    def prev_col(self):
        """Left"""
        self.index -= 1
    def next_col(self):
        """Right"""
        self.index += 1
    def prev_row(self):
        """Up"""
        self.index -= 9
    def next_row(self):
        """Down"""
        self.index += 9

    # TODO: Unsure if these are needed. Basically calls previous 4 methods with one call
    def prev_row_next_col(self):
        """Top Left"""
        pass
    def prev_row_next_col(self):
        """Top right"""
        pass
    def next_row_prev_col(self):
        """Bot left"""
        pass
    def next_row_next_col(self):
        """Bot right"""
        pass

if __name__ == "__main__":
    from listgrid import ListGrid
    from matrixgrid import MatrixGrid

    reference = False
    if reference:
        lines = [
            bot, box, top, box, top, box, div, box, top, box, top, 
            box, div, box, top, box, top, box, bot, ovr, num, top
        ]

        for line in lines:
            print(line)

    grids = False
    if grids:
        l = ListGrid.init_complete()
        print(l)
        m = MatrixGrid.init_complete()
        print(m)
        print(l == m)

    ui = UIGrid.init_complete()
    print(ui)
    # l = ListGrid.init_incomplete()
    # print(l)
    # m = MatrixGrid.init_incomplete()
    # print(m)
    # print(l == m)