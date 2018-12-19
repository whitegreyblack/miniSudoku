"""
chess.py

R N B K Q B N R
P P P P P P P P
P P P P P P P P
R N B K Q B N R
"""

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"
        
def pawn_move_fn(position, moves):
    moveset = set()
    if moves == 0:
        moveset.add((position.x, position.y+1))
    moveset.add((position.x, position.y+2))
    moveset.add((position.x+1, position.y+1))
    moveset.add((position.x-1, position.y+1))
    return moveset

pawn_movement = {
    # color, direction, unit, moves
    ("white", (0, 1), False, 0): (0, 1),
    ("white", (0, 1), False, 0): (0, 2),
    ("black", (0, -1), False, 0): (0, -1),
    ("black", (0, -1), False, 0): (0, -2),
}

class Moveset:
    def __init__(self, moves):
        self.moves = moves

class Unit:
    def __init__(self, name, position, moveset):
        self.name = name
        self.position = position
        self.num_moves = 0
        self.moveset = moveset

    def moves(self):
        return self.moveset(self.position, self.num_moves) 
        
    def move(self, position):
        self.position = position

    def __repr__(self):
        return f"{self.name}: {self.position}"

class Pawn(Unit):
    def __init__(self, position, moveset):
        super().__init__(self.__class__.__name__, position, moveset)

pawn = Pawn(Position(1,0), pawn_move_fn)
print(pawn, pawn.moves())
