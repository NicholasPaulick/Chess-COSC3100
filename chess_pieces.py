import pygame

class ChessPiece:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.image = None
        self.size = 100

    def draw(self, screen, square_size):
        if self.image:
            # Resize the image to fit the square size
            resized_image = pygame.transform.scale(self.image, (self.size, self.size))
            x = self.position[1] * square_size
            y = self.position[0] * square_size
            screen.blit(resized_image, (x, y))

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
