import sudoku
import curses
import curses.panel

# 37 x 21
chars=[]

def setup():
    curses.curs_set(0)
    chars.append(curses.ACS_BLOCK)                         # BLOCK
    chars.append(curses.ACS_BSSB)                          # UPPER RIGHT
    chars.append(curses.ACS_BSBS)                          # Horizontal Line
    chars.append(curses.ACS_BBSS)                          # UPPER LEFT
    chars.append(curses.ACS_TTEE)                          # TOP TEE
    chars.append(curses.ACS_BTEE)                          # BOT TEE
    chars.append(curses.ACS_VLINE)                         # SCAN LINE
    chars.append(curses.ACS_PLUS)                          # PLUS
    chars.append(curses.ACS_LTEE)                          # LEFT TEE
    chars.append(curses.ACS_RTEE)                          # RIGHT TEE

def makepuzzle():
    puzzle = sudoku.Grid()
    puzzle.fill()
    return puzzle

def fillgrid(g, p):
    for j in range(9):
        for i in range(9):
            g.addch(i*2+1, j*4+2, "{}".format(p.grid[i][j]))

def makegrid(l=19, c=37):
    '''
    creates the grid lines
    '''
    def row(i, char, outer, inner, step):                  # print magic
        start = step                                       # double for loop
        for m in range(outer):
            for n in range(inner):
                g.addch(i, start, char)
                start+=step
            start+=step
        return i+1

    def midrow(i=0):
        row(i, chars[4], 1, 2, 12)                         # outer down tees

        for i in range(1, l-1):

            if i % 2:                                      # inner grid
                row(i, '|', 3, 2, 4)                       # vertical bars 

            else:
                row(i, '-', 3, 11, 1)                      # horizontal bars
                row(i, ' ', 3, 2, 4)                       # pluses

        for i in range(1, l-1):                            # outer grid
            row(i, chars[6], 1, 2, 12)                     # vertical bars
            if i % 6 == 0:
                row(i, chars[2], 1, c-2, 1)                # horizontal lines
                row(i, chars[7], 1, 2, 12)                 # pluses
                row(i, chars[8], 1, 1, 0)                  # left tees
                g.addch(i, c-1, chars[9])                  # right tees
        row(i+1, chars[5], 1, 2, 12)                       # up tees

    g = curses.newwin(19, 37, 2, 3)
    g.border()
    index = midrow()
    return g

def makeboard(l=22, c=41):

    def addlabels(board):

        def letterstring():                                # top label
            return " ".join(list("  A B C D E F G H I"))

        board.addstr(1, 1, letterstring())                 # A-Z

        index, number = 3, 1
        for i in range(9):
            board.addstr(index, 2, "{}".format(number))    # 1-9
            number += 1
            index += 2

    board=curses.newwin(l,c,0,0)
    board.border()
    addlabels(board)                                       # grid labels
    return board

def play(b):
    b.getch()

def main(scr):

    puzzle = makepuzzle()                                  # Sudoku puzzle

    setup()
    board = makeboard()                                    # outer box
    grid = makegrid()                                      # inner box
    fillgrid(grid, puzzle)
    grid.overwrite(board)                                  # puts grid on top

    play(board)                                            # Solve it if you can!

if __name__ == "__main__":
    curses.wrapper(main)
