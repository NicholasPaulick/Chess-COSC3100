import pygame

class ChessBoard:
    def __init__(self):
        self.board_color_1 = (238, 238, 210)  # Light color
        self.board_color_2 = (118, 150, 86)   # Dark color
        self.board_size = 8
        self.square_size = 100  # Assuming a 800x800 window

    def draw(self, screen, offset_y=0):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.board_color_1 if (row + col) % 2 == 0 else self.board_color_2
                pygame.draw.rect(screen, color, (col * self.square_size, offset_y + row * self.square_size, self.square_size, self.square_size))