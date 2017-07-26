import sudoku
import curses

# 37 x 21
chars=[]
def printbottom(board, index, c):
    board.addstr(index, c, sudoku.box)
    board.addstr(index+1, c, sudoku.div)
    return index+2
def printcenter(board, index, c):
    for i in range(2):
        board.addstr(index, c, sudoku.box)
        board.addstr(index+1, c, sudoku.top)
        index += 2
    return index
def printlines(board, c):
    index = 2
    board.addstr(index,c,sudoku.bot)
    index += 1
    for i in range(2):
        index=printcenter(board, index, c)
        index=printbottom(board, index, c)
    index=printcenter(board, index, c)
    board.addstr(index, c, sudoku.box)
    board.addstr(index+1, c, sudoku.bot)
def letterstring():
    string=" ".join(list("  A B C D E F G H I"))
    return string
def makeboard():
    board=curses.newwin(22,41,0,0)
    board.border()
    board.addstr(1,1,letterstring())
    index=3
    number=1
    for i in range(9):
        board.addstr(index, 1, "{}".format(number))
        number+=1
        index+=2
    col = 3
    printlines(board, col)
    return board
def setup():
    curses.curs_set(0)
    chars.append(curses.ACS_BLOCK)
    chars.append(curses.ACS_BSSB)

def main(scr):
    scr.addstr(1,1,"{}".format(scr.getmaxyx()))
    
    # adds ACS characterset to build board
    setup()
    scr.addstr(2, 1,"making border")
    board = makeboard() 
    char = board.getch() 


if __name__ == "__main__":
    curses.wrapper(main)
