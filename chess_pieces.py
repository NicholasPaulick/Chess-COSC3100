class ChessPiece:
    def __init__(self, position, color):
        self.row, self.col = position
        self.color = color
        self.image = None

    def move(self, new_position):
        self.row, self.col = new_position

    def get_pygame_pos(self, square_size):
        return (self.col * square_size, (7 - self.row) * square_size)

class Pawn(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = '♙' if color == 'white' else '♟'

class King(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = '♔' if color == 'white' else '♚'

class Queen(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = '♕' if color == 'white' else '♛'

class Bishop(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = '♗' if color == 'white' else '♝'

class Knight(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = '♘' if color == 'white' else '♞'

class Rook(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = '♖' if color == 'white' else '♜'