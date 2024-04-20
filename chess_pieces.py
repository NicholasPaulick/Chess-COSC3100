import pygame


class ChessPiece:
    def __init__(self, position, color):
        self.position = position  # Position is now used for initial setup only
        self.color = color
        self.image = None
        self.size = 100  # Size for the pieces

    def draw(self, screen, x, y, offset_y=0):
        if self.image:
            resized_image = pygame.transform.scale(self.image, (self.size, self.size))
            screen.blit(resized_image, (x, y + offset_y))  # Apply offset_y here


class Pawn(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = pygame.image.load(f'images/{color}-pawn.png')

class King(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = pygame.image.load(f'images/{color}-king.png')

class Queen(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = pygame.image.load(f'images/{color}-queen.png')

class Bishop(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = pygame.image.load(f'images/{color}-bishop.png')

class Knight(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = pygame.image.load(f'images/{color}-knight.png')

class Rook(ChessPiece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.image = pygame.image.load(f'images/{color}-rook.png')
