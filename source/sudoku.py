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
    def __init__(self, grid: list=None, build: bool=True) -> None:
        super().__init__(grid, build)
        self.build_border_tiny()
        self.build_border_small()
        self.build_border_large()

    def build_border_tiny(self):
        self.border_tiny = [[' ' for _ in range(80)] for _ in range(25)]
        self.border_tiny[0][0] = HEAVY_TLC
        self.border_tiny[0][24] = HEAVY_TRC
        self.border_tiny[12][0] = HEAVY_BLC
        self.border_tiny[12][24] = HEAVY_BRC
        # vertical bars
        for y in range(1, 12):
            for x in (0, 24):
                self.border_tiny[y][x] = HEAVY_VBAR
            for x in (8, 16):
                self.border_tiny[y][x] = LIGHT_VBAR
        for x in range(1, 24):
            for y in (0, 12):
                self.border_tiny[y][x] = HEAVY_HBAR
            for y in (4, 8):
                self.border_tiny[y][x] = LIGHT_HBAR

        for y in (4, 8):
            for x in (8, 16):
                self.border_tiny[y][x] = LIGHT_CRS

    def build_border_small(self):
        self.border_small = [[' ' for _ in range(80)] for _ in range(25)]
        self.border_small[0][0] = HEAVY_TLC
        self.border_small[0][44] = HEAVY_TRC
        self.border_small[24][0] = HEAVY_BLC
        self.border_small[24][44] = HEAVY_BRC
        
        for y in range(1, 23):
            for x in range(14, 44, 14):
                if x % 14 == 0:
                    self.border_small[y][x] = HEAVY_VBAR
                else:
                    self.border_small[y][x] = LIGHT_VBAR

        # horizontal bars
        for y in range(0, 25, 8):
            heavy = y % 6 == 0
            for x in range(1, 44):
                self.border_small[y][x] = HEAVY_HBAR if heavy else LIGHT_HBAR

    def build_border_large(self):
        self.border_large = [[' ' for _ in range(73)] for _ in range(37)]
        self.border_large[0][0] = HEAVY_TLC
        self.border_large[0][72] = HEAVY_TRC
        self.border_large[36][0] = HEAVY_BLC
        self.border_large[36][72] = HEAVY_BRC

    @property
    def cursor(self):
        yield 1, 1, "[ ]"

    @property
    def values_tiny_board(self) -> str:
        for by in range(3):
            for bx in range(3):
                for y in range(3):
                    for x in range(3):
                        val = self.grid[by*27+bx*3+y*9+x] # access by grid index
                        if val != 0:
                            yield bx*8+x*2+2, by*4+y*1+1, str(val) # access by row, col, block

    @property
    def values_small_board(self) -> str:
        for by in range(3):
            for bx in range(3):
                for y in range(3):
                    for x in range(3):
                        val = self.grid[by*27+bx*3+y*9+x] # access by grid index
                        if val != 0:
                            yield bx*8+x*2+1, by*4+y*1+1, str(val) # access by row, col, block
    
    @property
    def border_tiny_board(self) -> str:
        for y, row in enumerate(self.border_tiny):
            for x, val in enumerate(row):
                yield x, y, val
    
    @property
    def border_small_board(self) -> str:
        for y, row in enumerate(self.border_small):
            for x, val in enumerate(row):
                yield x, y, val

    @property
    def values(self) -> str:
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
    def border(self) -> str:
        g = [[' ' for _ in range(73)] for _ in range(37)]
        g[0][0] = HEAVY_TLC
        g[0][72] = HEAVY_TRC
        g[36][0] = HEAVY_BLC
        g[36][72] = HEAVY_BRC

        # goes down from 0 -> y
        # for y in range(1, 36):
        #     for x in range(8, 64, 8):
        #         print(y, x)
        #         g[y][x] = HEAVY_VBAR if x % 24 == 0 else LIGHT_VBAR
        #     # g[y][0] = HEAVY_VBAR
        #     # g[y][8] = LIGHT_VBAR
        #     # g[y][16] = LIGHT_VBAR
        #     # g[y][24] = HEAVY_VBAR
        #     # g[y][32] = LIGHT_VBAR
        #     # g[y][40] = LIGHT_VBAR
        #     # g[y][48] = HEAVY_VBAR
        #     # g[y][56] = LIGHT_VBAR
        #     # g[y][64] = LIGHT_VBAR
        #     # g[y][72] = HEAVY_VBAR
        #     if y % 12 == 0:
        #         g[y][0] = HEAVY_ABR
        #         g[y][72] = HEAVY_EBR
        return ''.join(''.join(r) for r in g)

        # # horizontal bars
        # for x in range(0, 37, 4):
        #     symbols = LIGHT_HBAR * 71
        #     if x % 12 == 0:
        #         symbols = HEAVY_HBAR * 71
        #     t.puts(1, x, symbols)

        # for x in (24, 48):
        #     for y in range(4, 33, 4):
        #         t.puts(x, y, HEAVY_VBAR)

        # for x in range(8, 74, 8):
        #     if x % 24 != 0:
        #         for y in range(4, 33, 4):
        #             if y % 12 != 0:
        #                 t.puts(x, y, LIGHT_CRS)

        # for x in (24, 48):
        #     for y in (12, 24):
        #         t.puts(x, y, HEAVY_CRS)

        # # t.puts(8, 0, HLIGHT_TBR)
        # t.puts(24, 0, HEAVY_TBR)
        # t.puts(48, 0, HEAVY_TBR)
        # t.puts(24, 36, "\u2538")
        # t.puts(48, 36, "\u2538")

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
    escape_codes = [t.TK_Q, t.TK_ESCAPE, 224]

    t.open()
    # t.set("window.size=73x37, window.title='Sudoku'")

    for i, j, s in list(ui.border_tiny_board):
        t.puts(i, j, s)
    
    print(*list(ui.cursor))

    for i, j, s in list(ui.values_tiny_board):
        t.puts(i, j, s)

    t.puts(*list(ui.cursor)[0])

    t.refresh()
    c = t.read()
