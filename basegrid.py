"""
Basegrid.py

Implements shared methods between list and matrix grids.
"""
import tool
class BaseGrid:
    def __init__(self, grid: list=None, build: bool=True) -> None:
        """
        If no grid is given, will build a new list. If board is not valid
        on init, then the board will be filled until it is valid or an error
        is thrown.
        """
        self.grid = grid
        empty = not self.grid
        if empty:
            self.build_empty_board()
        if not self.valid_board and build:
            self.retrieve_empty_cells(empty)
            if not self.fill_board() and not empty:
                raise ValueError("Given board was incorrect")

    def __str__(self):
        return self.board
    
    def __repr__(self):
        return self.board

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.grid == other.grid
        return hash(self) == hash(other)

    @property
    def valid_board(self):
        """Determines if the board is in a valid state"""
        self.check_grid()
        return self.validate()

    def possible_values(self, cell):
        """
        Returns values not located in the row, column, or block for input
        cell index.
        """
        vals = set(j + 1 for j in range(9))
        vals -= set(self.row(cell[0]))
        vals -= set(self.col(cell[1]))
        vals -= set(self.block(cell[2]))
        vals -= {0}
        return vals

    def validate(self):
        for p in 'row col block'.split():
            if not all(self.check(p, v) for v in range(9)):
                return False
        return True

    def check(self, prop, val):
        p = getattr(self, prop)(val)
        return len(p) == len(set(p) - {0}) == 9

    @property
    def rows_valid(self) -> bool:
        """Returns a list with values indicating validness for each row"""
        return all(self.check('row', r) for r in range(9))
    
    @property
    def cols_valid(self) -> bool:
        """Returns the values of all columns indicating validness"""
        return all(self.check('col', c) for c in range(9))

    @property
    def blocks_valid(self) -> bool:
        """
        Returns a value for each block in the grid determining each individual
        block validness
        """
        return all(self.check('block', b) for b in range(9))