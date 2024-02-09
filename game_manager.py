import pygame
from chess_pieces import Pawn, King, Queen, Bishop, Knight, Rook

class GameManager:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.selected_square = None
        self.turn = 'white'

    def setup_board(self):
        # Place black pieces
        self.board[0][0] = Rook((0, 0), 'black')
        self.board[0][1] = Knight((0, 1), 'black')
        self.board[0][2] = Bishop((0, 2), 'black')
        self.board[0][3] = Queen((0, 3), 'black')
        self.board[0][4] = King((0, 4), 'black')
        self.board[0][5] = Bishop((0, 5), 'black')
        self.board[0][6] = Knight((0, 6), 'black')
        self.board[0][7] = Rook((0, 7), 'black')
        for col in range(8):
            self.board[1][col] = Pawn((1, col), 'black')

        # Place white pieces
        self.board[7][0] = Rook((7, 0), 'white')
        self.board[7][1] = Knight((7, 1), 'white')
        self.board[7][2] = Bishop((7, 2), 'white')
        self.board[7][3] = Queen((7, 3), 'white')
        self.board[7][4] = King((7, 4), 'white')
        self.board[7][5] = Bishop((7, 5), 'white')
        self.board[7][6] = Knight((7, 6), 'white')
        self.board[7][7] = Rook((7, 7), 'white')
        for col in range(8):
            self.board[6][col] = Pawn((6, col), 'white')

    def draw_pieces(self, screen, square_size):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    piece.draw(screen, square_size)

    def select_piece(self, row, col):
        if self.board[row][col] and self.board[row][col].color == self.turn:
            self.selected_piece = self.board[row][col]
            self.selected_square = (row, col)
            return True
        return False

    def move_piece(self, row, col):
        if self.selected_piece:
            # Update the board and the piece's position
            self.board[self.selected_piece.position[0]][self.selected_piece.position[1]] = None
            self.board[row][col] = self.selected_piece
            self.selected_piece.position = (row, col)
            self.selected_piece = None
            self.selected_square = None  # Deselect square after moving
            # Switch turns
            self.turn = 'black' if self.turn == 'white' else 'white'

    # Add a method to highlight the selected square
    def highlight_selected_square(self, screen, square_size):
        if self.selected_square:
            highlight_color = (0, 255, 255)  # Light blue for highlighting
            x = self.selected_square[1] * square_size
            y = self.selected_square[0] * square_size
            pygame.draw.rect(screen, highlight_color, (x, y, square_size, square_size))
            piece = self.board[self.selected_square[0]][self.selected_square[1]]
            if piece:
                piece.draw(screen, square_size)
