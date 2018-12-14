"""
Matrixgrid.py

Implements a 2d matrix and methods to access values in matrix
"""
import tool
from basegrid import BaseGrid

class MatrixGrid(BaseGrid):
    """Underlying datatype to hold values is a list of lists"""
    def __hash__(self) -> int:
        return tool.list_to_str(tool.list_to_str for row in self.grid)

    @property
    def board(self) -> bool:
        """Allows access of board representation as a string property"""
        divider = "+" + "-" * 23 + "+"
        b = [divider]
        for r in range(9):
            row = []
            for c in range(3):
                s = c * 3
                row.append(' '.join(str(i) if i > 0 else ' '
                                        for i in self.grid[r][s:s+3]))
            b.append(f"| {row[0]} | {row[1]} | {row[2]} |")
            if (r + 1) % 3 == 0:
                b.append(divider)
        return "\n".join(b)

    def build_empty_board(self) -> None:
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def check_grid(self) -> None:
        """Returns a value indicating if board has number of correct cells"""
        if len(self.grid) != 9:
            raise ValueError("Grid does not have corrent length rows")
        for row in self.grid:
            if len(row) != 9:
                raise valueError("Grid does not have corrent length columns")

    def retrieve_empty_cells(self, empty: bool) -> None:
        self.cells = []
        for r in range(9):
            row = []
            for c in range(9):
                if empty or self.grid[r][c] == 0:
                    b = tool.block_counter(r, c)
                    row.append((r, c, b))
            self.cells += row if r % 2 == 0 else row[::-1]

    def fill_board(self) -> bool:
        """Used to fill values on an empty/partial board"""
        if self.valid_board:
            return True

        cell = self.cells.pop(0)
        r = cell[0]
        c = cell[1]
        vals = self.possible_values(cell)

        for v in tool.shuffle(vals):
            self.grid[r][c] = v
            if self.fill_board():
                return True
            self.grid[r][c] = 0

        # no values fit. Put the cell back and try again.
        self.cells.insert(0, cell)
        return False

    def row(self, rownum: int) -> list:
        """Returns the values of row with the given row number"""
        return self.grid[rownum]

    def col(self, colnum: int) -> list:
        """
        Returns a column from the 1d grid corresponding to the column number
        passed in.
        """
        return [self.grid[r][colnum] for r in range(9)]

    def block(self, blocknum: int) -> list:
        """
        Returns a block as a 1d array from the 1d grid corresponding to the
        block number passed in as a parameter
        """
        block = []
        r = blocknum // 3 * 3
        c = blocknum % 3 * 3
        for row in self.grid[r:r+3]:
            for val in row[c:c+3]:
                block.append(val)
        return block

    @classmethod
    def init_from(cls, array: list) -> object:
        """Build MatrixGrid from a given 1d array"""
        return cls(tool.split_rows(array))

    @classmethod
    def from_array(cls, array: list) ->object:
        return cls(tool.split_rows(array))

    @classmethod
    def init_complete(cls) -> object:
        """
        Builds a new ListGrid with a complete grid passed in. Used to test
        the ListGrid."""
        return cls(tool.test_complete)

    @classmethod
    def init_incomplete(cls) -> object:
        """
        Builds a new ListGrid with an incomplete grid passed in. Used to test
        the ListGrid.
        """
        return cls(tool.test_incomplete)

    @classmethod
    def init_incorrect(cls) -> object:
        """
        Builds a new ListGrid with a grid that is impossible to complete. Used
        to test the ListGrid."""
        return cls(tool.test_incorrect)

    # @classmethod
    # def from_json(self, dictionary):
    #     return Grid()

    # def to_json(self):
    #     """
    #     With json, the board can be represented with all filled/given cells as
    #     a position index with value and any positions not in the given data
    #     considered as unfilled
    #     """
    #     return

if __name__ == "__main__":
    m = MatrixGrid(tool.test_incomplete)
    print(m)