import os

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []
        

# inherits from Piece
class Pawn(Piece):
    def __init__(self, color):
        if color == 'white':
            # based on how coordinates work in pygame (y top to bottom)
            self.dir = -1
        else:
            self.dir = 1
        # enpessant
        self.en_pessant = False
        # call the mother object with specific attributes
        super().__init__('pawn', color, 1.0)

class Knight(Piece):
    def __init__(self, color):
        # chess piece's values are rlly important for AI
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        # wanna state in some sense that they are more important than knights
        super().__init__('bishop', color, 3.01)

class Rook(Piece):
    def __init__(self, color):
        # wanna state in some sense that they are more important than knights
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        # state that's the more important by a lot (inf could work 2)
        super().__init__('king', color, 100000)