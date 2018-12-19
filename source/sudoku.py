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
import tool
from listgrid import ListGrid
from matrixgrid import MatrixGrid
from bearlibterminal import terminal as t

class Box:
    HBR = "\u2500"
    VBR = "\u2502"
    TBR = "\u252C"
    ABR = "\u251C"
    EBR = "\u2524"
    TLC = "\u250C"
    TRC = "\u2514"
    BLC = "\u2510"
    BRC = "\u2518"

HEAVY_TLC = "\u250F"
HEAVY_TRC = "\u2513"
HEAVY_BLC = "\u2517"
HEAVY_BRC = "\u251B"
HEAVY_HBAR = "\u2501"
HEAVY_VBAR = "\u2503"
HEAVY_TBR = "\u2533"
HEAVY_ABR = "\u2523"
HEAVY_EBR = "\u252B"
HEAVY_OBR = "\u253B"
HLIGHT_TBR = "\u252F"
LIGHT_VBAR = "\u2502"
LIGHT_HBAR = "\u2500"
HLIGHT_CRS = "\u2542"
LHEAVY_CRS = "\u253F"
LIGHT_CRS = "\u253C"
HEAVY_CRS = "\u254B"

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
    def terminal(self) -> str:
        for by in range(3):
            for bx in range(3):
                for y in range(3):
                    for x in range(3):
                        val = self.grid[by*27+bx*3+y*9+x]
                        if val != 0:
                            rows = []
                            for col in range(3):
                                if col == 1:
                                    rows.append(f"   [color=orange]{val}[/color]  ")
                                else:
                                    rows.append(f" " * 7)
                            yield bx*24+x*8+1, by*12+y*4+1, "\n".join(rows)
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

    # TODO: Unsure if these are needed. Basically calls previous 4 methods
    #       with one call instead of two
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

    ui = UIGrid.init_incomplete(build=False)
    print(ui)
    # l = ListGrid.init_incomplete()
    # print(l)
    # m = MatrixGrid.init_incomplete()
    # print(m)
    # print(l == m)
    escape_codes = [t.TK_Q, t.TK_ESCAPE, 224]

    t.open()
    t.set("window.size=73x37, window.title='Sudoku'")
    # for i, j, s in list(ui.terminal):
    #     t.puts(i, j, s)
    # for index, string in enumerate(list(ui.board)):
    #     i, j = index // 3, index % 3
    #     t.puts(i + i * 6, 0 + 8 * j, string)
    # t.puts(1, 0, ui.board)
    # t.puts(24, 0, ui.board)
    # t.puts(48, 0, ui.board)
    # t.puts(0, 12, ui.board)
    # t.puts(24, 12, ui.board)
    # t.puts(48, 12, ui.board)
    # t.puts(0, 24, ui.board)
    # t.puts(24, 24, ui.board)
    # t.puts(48, 24, ui.board)

    # for i in range(0, 74, 8):
    #     print(i)

    ystepbig = 24
    ystepsmall = 8

    for y in range(0, 36):
        for x in range(0, 74):
            ymod = y % 4 == 0
            xmod = x % 8 == 0
            if xmod and ymod:
                pass
            elif xmod:
                pass
            elif ymod:
                pass
            else:
                pass

    t.puts(0, 0, HEAVY_TLC)
    t.puts(72, 0, HEAVY_TRC)

    t.puts(0, 36, HEAVY_BLC)
    t.puts(72, 36, HEAVY_BRC)

    # goes down from 0 -> y
    for y in range(1, 36):
        t.puts(0, y, HEAVY_VBAR)
        t.puts(8, y, LIGHT_VBAR)
        t.puts(16, y, LIGHT_VBAR)
        t.puts(24, y, HEAVY_VBAR)
        t.puts(32, y, LIGHT_VBAR)
        t.puts(40, y, LIGHT_VBAR)
        t.puts(48, y, HEAVY_VBAR)
        t.puts(56, y, LIGHT_VBAR)
        t.puts(64, y, LIGHT_VBAR)
        t.puts(72, y, HEAVY_VBAR)
        if y % 12 == 0:
            t.puts(0, y, HEAVY_ABR)
            t.puts(72, y, HEAVY_EBR)

    # horizontal bars
    for x in range(0, 37, 4):
        symbols = LIGHT_HBAR * 71
        if x % 12 == 0:
            symbols = HEAVY_HBAR * 71
        t.puts(1, x, symbols)

    for x in (24, 48):
        for y in range(4, 33, 4):
            t.puts(x, y, HEAVY_VBAR)

    for x in range(8, 74, 8):
        if x % 24 != 0:
            for y in range(4, 33, 4):
                if y % 12 != 0:
                    t.puts(x, y, LIGHT_CRS)

    for x in (24, 48):
        for y in (12, 24):
            t.puts(x, y, HEAVY_CRS)

    # t.puts(8, 0, HLIGHT_TBR)
    t.puts(24, 0, HEAVY_TBR)
    t.puts(48, 0, HEAVY_TBR)
    t.puts(24, 36, "\u2538")
    t.puts(48, 36, "\u2538")

    for i, j, s in list(ui.terminal):
        t.puts(i, j, s)

    t.refresh()
    c = t.read()
