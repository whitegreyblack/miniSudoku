"""
Listgrid.py

Implements a 1D list and methods to represent 2D matrix space
"""
import tool
from basegrid import BaseGrid

class ListGrid(BaseGrid):
    """Underlying datatype to hold values is a list"""
    def __hash__(self) -> int:
        return tool.list_to_str(tool.list_to_str(r) 
                                    for r in tool.split_rows(self.grid))

    @property
    def board(self) -> str:
        """Allows access of board representation as a string property"""
        divider = "+" + "-" * 23 + "+"
        b = [divider]
        for i in range(9):
            r = []
            for j in range(3):
                s = tool.index_counter(i, j * 3)
                r.append(' '.join(str(i) if i > 0 else ' '
                                    for i in self.grid[s:s+3]))
            b.append(f"| {r[0]} | {r[1]} | {r[2]} |")
            if (i + 1) % 3 == 0:
                b.append(divider)
        return "\n".join(b)

    def build_empty_board(self) -> None:
        self.grid = [0 for _ in range(81)]

    def check_grid(self) -> None:
        """Returns a value indicating if board has number of correct cells"""
        if not len(self.grid) == 81:
            raise ValueError("Grid does not have 81 elements. Aborting")

    def retrieve_empty_cells(self, empty: bool) -> None:
        self.cells = []
        for r in range(9):
            row = []
            for c in range(9):
                index = tool.index_counter(r, c)
                if empty or self.grid[index] == 0:
                    block = tool.block_counter(r, c)
                    row.append((r, c, block, index))
            self.cells += row if r % 2 == 0 else row[::-1]

    def fill_board(self) -> bool:
        """Used to fill values on an empty board"""
        if self.valid_board:
            return True

        cell = self.cells.pop(0)
        i = cell[3]
        vals = self.possible_values(cell)

        for v in tool.shuffle(vals):
            self.grid[i] = v
            if self.fill_board():
                return True
            self.grid[i] = 0

        # no values fit. Put the cell back and try again.
        self.cells.insert(0, cell)
        return False

    def cell(self, index: int) -> int:
        return self.grid[index]

    def row(self, row: int) -> list:
        """Returns the values of row with the given row number"""
        index_start = row * 9
        return self.grid[index_start:index_start+9]

    def col(self, col: tuple) -> list:
        """
        Returns a column from the 1d grid corresponding to the column number
        passed in.
        """
        return self.grid[col::9]

    def block(self, block: tuple) -> list:
        """
        Returns a block as a 1d array from the 1d grid corresponding to the
        block number passed in as a parameter
        """
        b = []
        for j in range(3):
            index = block * 3 + j * 9 + 18 * (block // 3)
            for val in self.grid[index:index+3]:
                b.append(val)
        return b

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
    def init_from(cls, matrix: list) -> object:
        """Build ListGrid from a given 2d matrix"""
        return cls(tool.flatten(matrix))

    @classmethod
    def from_matrix(cls, matrix: list) -> object:
        """Builds a new ListGrid with a given 2d matrix"""
        return cls(tool.matrix_to_array(matrix))

    @classmethod
    def init_complete(cls) -> object:
        """
        Builds a new ListGrid with a complete grid passed in. Used to test
        the ListGrid."""
        return cls.from_matrix(tool.test_complete)

    @classmethod
    def init_incomplete(cls) -> object:
        """
        Builds a new ListGrid with an incomplete grid passed in. Used to test
        the ListGrid.
        """
        return cls.from_matrix(tool.test_incomplete)

    @classmethod
    def init_incorrect(cls) -> object:
        """
        Builds a new ListGrid with a grid that is impossible to complete. Used
        to test the ListGrid."""
        return cls.from_matrix(tool.test_incorrect)

if __name__ == "__main__":
    # TODO: move to tests
    # m = ListGrid(tool.flatten(tool.test_complete))
    # n = ListGrid.init_from(tool.test_complete)
    # print(m)
    # print(n)
    # print(m==n)
    # m = ListGrid(tool.flatten(tool.test_incomplete))
    # n = ListGrid.init_from(tool.test_incomplete)
    # l = ListGrid.init_incomplete()
    # print(m)
    # print(n)
    # print(l)
    # print(m==n==l)
    m = ListGrid()
    print(m)