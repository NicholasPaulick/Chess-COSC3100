import pygame
from chess_pieces import Pawn, King, Queen, Bishop, Knight, Rook
from move_generator import MoveGenerator
import random

class GameManager:
    def __init__(self, chess_board):
        self.chess_board = chess_board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        # Initialize last_move_white and last_move_black to None or a suitable default value
        self.last_move_white = None  # Initialize as None or a default value indicating no move has been made
        self.last_move_black = None  # Initialize as None or a default value indicating no move has been made
        self.move_history = []
        self.move_generator = MoveGenerator(self.board)
        self.turn = 'white'
        self.setup_board()
        
        # Initialize the timer
        self.total_time = 600  # Total time for the game in seconds (e.g., 10 minutes)
        self.start_ticks = pygame.time.get_ticks()  # Starting tick for the timer

        self.setup_board()

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

    def draw_pieces(self, screen, square_size, offset_y=0):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    # Calculate the exact position based on the square size and offset
                    x = col * square_size
                    y = row * square_size
                    piece.draw(screen, x, y, offset_y)
    
    def handle_board_click(self, pos, offset_y):
        square_size = self.chess_board.square_size
        col = pos[0] // square_size
        row = (pos[1] - offset_y) // square_size

        # Check if the click is within the bounds of the board
        if 0 <= row < 8 and 0 <= col < 8:
            if self.selected_piece:
                # Check if the selected square is a valid move
                if (row, col) in self.valid_moves:
                    # Execute the move
                    self.move_piece(row, col)
                else:
                    # If clicked on another of the player's pieces, select that piece instead
                    # Or deselect the current piece if it's clicked again
                    self.select_piece(row, col)
            else:
                # No piece currently selected, attempt to select a piece
                self.select_piece(row, col)

    def select_piece(self, row, col):
        # Check if the clicked square contains a piece of the current player's color
        if self.board[row][col] and self.board[row][col].color == self.turn:
            # Check if the same piece is selected again (deselecting it)
            if self.selected_piece == self.board[row][col]:
                self.selected_piece = None
                self.selected_square = None
                self.valid_moves = []
                return False  # Indicate that a piece was deselected
            else:
                # Selecting a new piece
                self.selected_piece = self.board[row][col]
                self.selected_square = (row, col)
                # Retrieve the last move based on the current turn
                last_move = self.last_move_white if self.turn == 'white' else self.last_move_black
                # Pass last_move to get_valid_moves
                self.valid_moves = self.move_generator.get_valid_moves(self.selected_piece, last_move)
                return True  # Indicate that a piece was selected
        else:
            # Clicked on an empty square or an opponent's piece without a piece currently selected
            self.selected_piece = None
            self.selected_square = None
            self.valid_moves = []
            return False

    def move_piece(self, row, col, piece=None):
        # If a piece is specified, use it; otherwise, use the currently selected piece
        moving_piece = piece if piece else self.selected_piece
    
        #if not moving_piece or (row, col) not in self.valid_moves:
        #    # If no piece is specified or available, or the target square isn't a valid move, do nothing
        #    return False
    
        start_pos = moving_piece.position
        target_square = self.board[row][col]
    
        # Execute the move
        self.board[start_pos[0]][start_pos[1]] = None  # Clear the start position
        self.board[row][col] = moving_piece  # Place the piece at the new position
        moving_piece.position = (row, col)  # Update the piece's position attribute
    
        # Handle special moves (e.g., capturing, en passant, promotion) here
        # This example doesn't include those details, but they would be handled based on your game's rules
    
        # Append the move to the move history
        move_record = (moving_piece, start_pos, (row, col), target_square)
        self.move_history.append(move_record)
    
        # Update last move tracking
        last_move = (start_pos, (row, col))
        if self.turn == 'white':
            self.last_move_white = last_move
        else:
            self.last_move_black = last_move
    
        # Switch turns
        self.turn = 'black' if self.turn == 'white' else 'white'
    
        # Deselect the piece and clear valid moves after moving
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
    
        # Move was successful
        return True


    def _get_last_move(self):
        # Helper method to get the last move based on the current turn
        return self.last_move_white if self.turn == 'black' else self.last_move_black
        

    # Add a method to highlight the selected square
    def highlight_selected_square(self, screen, square_size, offset_y=0):
        if self.selected_square:
            row, col = self.selected_square
            x = col * square_size
            y = row * square_size  # Calculate y without adding offset_y yet

            # Draw the highlight rectangle
            highlight_color = (0, 255, 255)  # Example highlight color
            pygame.draw.rect(screen, highlight_color, (x, y + offset_y, square_size, square_size))

            # Draw the piece, applying offset_y correctly
            piece = self.board[row][col]
            if piece:
                piece.draw(screen, x, y, offset_y)  # offset_y is applied correctly inside piece.draw()

    def highlight_valid_moves(self, screen, square_size, offset_y=0):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.rect(screen, (255, 0, 0), (col * square_size, row * square_size + offset_y, square_size, square_size), 3)


    def undo_move(self):
        if not self.move_history:
            # No moves to undo
            return False  # Indicate that no move was undone
        
        # Retrieve the last move from the move history
        moved_piece, start_pos, end_pos, captured_piece = self.move_history.pop()
        
        # Move the moved piece back to its start position
        self.board[end_pos[0]][end_pos[1]] = None  # Clear the target position
        self.board[start_pos[0]][start_pos[1]] = moved_piece  # Place the moved piece back
        moved_piece.position = start_pos  # Update the piece's position attribute
        
        # Restore any captured piece, if any
        if captured_piece:
            self.board[end_pos[0]][end_pos[1]] = captured_piece
            captured_piece.position = end_pos
        
        # Update the turn back to the player who made the move
        self.turn = 'white' if self.turn == 'black' else 'black'
        
        # Clear the selection and valid moves as the move has been undone
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        
        return True  # Indicate that a move was successfully undone


    def get_all_possible_moves(self, color):
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    valid_moves = self.move_generator.get_valid_moves(piece, self._get_last_move())
                    for move in valid_moves:
                        all_moves.append((piece, move))
        return all_moves

    def execute_move(self, piece, target_pos):
        # Save the current state before making the move
        original_pos = piece.position
        # Update the board: Remove the piece from its original position
        self.board[original_pos[0]][original_pos[1]] = None
        # Capture any piece at the target position (if any)
        captured_piece = self.board[target_pos[0]][target_pos[1]]
        # Place the piece at the new position
        self.board[target_pos[0]][target_pos[1]] = piece
        # Update the piece's position
        piece.position = target_pos
        # Record the move (optional, for undo functionality or history)
        self.move_history.append((piece, original_pos, target_pos, captured_piece))

        # Switch turns
        self.turn = 'black' if self.turn == 'white' else 'white'
        return captured_piece

    def is_game_over(self):
        # Check for checkmate or stalemate
        white_moves = self.get_all_possible_moves('white')
        black_moves = self.get_all_possible_moves('black')

        if not white_moves and self.turn == 'white':
            # No valid moves for white, so black wins
            return True
        elif not black_moves and self.turn == 'black':
            # No valid moves for black, so white wins
            return True
        else:
            # Game is not over
            return False
    
    def restart_game(self, chess_board):
        self.__init__(chess_board)