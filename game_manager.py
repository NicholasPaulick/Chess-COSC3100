import pygame
from chess_pieces import Pawn, King, Queen, Bishop, Knight, Rook
from move_generator import MoveGenerator

class GameManager:
    def __init__(self, chess_board):
        self.chess_board = chess_board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        self.move_history = [None]
        self.move_generator = MoveGenerator(self.board)
        self.turn = 'white'
        self.setup_board()
        
        # Initialize the timer
        self.total_time = 600  # Total time for the game in seconds (e.g., 10 minutes)
        self.start_ticks = pygame.time.get_ticks()  # Starting tick for the timer

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
                last_move = self.move_history[len(self.move_history)-1]
                # Pass last_move to get_valid_moves
                self.valid_moves = self.get_valid_moves(self.selected_piece, last_move)
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
        moving_piece.move((row, col))  # Update the piece's position using the move method
    
        # Handle special moves (e.g., capturing, en passant, promotion) here
        # Check for pawn promotion
        if isinstance(moving_piece, Pawn):
            if moving_piece.color == 'white' and row == 0:
                # Promote white pawn
                promotion_piece = Queen  # Change this to the desired promotion piece
                self.promote_pawn(moving_piece, promotion_piece)
            elif moving_piece.color == 'black' and row == 7:
                # Promote black pawn
                promotion_piece = Queen  # Change this to the desired promotion piece
                self.promote_pawn(moving_piece, promotion_piece)
    
        # Append the move to the move history
        move_record = (moving_piece, start_pos, (row, col), target_square, self.turn)
        self.move_history.append(move_record)
    
        # Switch turns
        self.turn = 'black' if self.turn == 'white' else 'white'
    
        # Deselect the piece and clear valid moves after moving
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
    
        # Move was successful
        return True

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
        if self.move_history[len(self.move_history)-1] == None:
            # No moves to undo
            return False  # Indicate that no move was undone
        
        # Retrieve the last move from the move history
        moved_piece, start_pos, end_pos, captured_piece, color = self.move_history.pop()
        
        # Move the moved piece back to its start position
        self.board[end_pos[0]][end_pos[1]] = None  # Clear the target position
        self.board[start_pos[0]][start_pos[1]] = moved_piece  # Place the moved piece back
        moved_piece.position = start_pos  # Update the piece's position attribute
        
        # Restore any captured piece, if any
        if captured_piece:
            self.board[end_pos[0]][end_pos[1]] = captured_piece
            captured_piece.position = end_pos
        
        # Update the turn back to the player who made the move
        self.turn = color
        
        return True  # Indicate that a move was successfully undone

    def get_valid_moves(self, piece, last_move):
        moves = self.get_moves(piece, last_move)
        valid_moves = []
        for move in moves:
            self.move_piece(move[0], move[1], piece)
            if not self.is_check(piece.color):
                valid_moves.append(move)
            self.undo_move()
        self.selected_piece = piece
        return valid_moves

    def is_check(self, color):
        """
        Check if the king of the given color is in check.
        """
        king_position = self.get_king_position(color)
        if king_position is None:
            return False  # No king on the board, so not in check
    
        opponent_color = 'white' if color == 'black' else 'black'
        opponent_moves = self.get_all_possible_moves(opponent_color)
        for move in opponent_moves:
            if move == king_position:
                return True
        return False

    def get_king_position(self, color):
        """
        Get the position of the king for the given color, or None if the king is not found.
        """
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None  # King not found

    def is_checkmate(self, color):
        """
        Check if the player with the given color is in checkmate.
        """
        if not self.is_check(color):
            return False

        # If in check, check if there are any valid moves to get out of check
        valid_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    moves = self.get_valid_moves(piece, None)
                    for move in moves:
                        valid_moves.append((piece, move))
        if not valid_moves:
            return True  # No valid moves, it's checkmate

    def get_all_possible_moves(self, color):
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    moves = self.get_moves(piece, self.move_history[-1])
                    all_moves.extend(moves)
        return all_moves

    def get_moves(self, piece, last_move):
        if isinstance(piece, Pawn):
            return self.move_generator.move_tables[type(piece)](piece, last_move)
        else:
            return self.move_generator.move_tables[type(piece)](piece)

    def evaluate_board(self):
        piece_values = {'Pawn': 1, 'Knight': 3, 'Bishop': 3, 'Rook': 5, 'Queen': 9, 'King': 0}
        board_value = 0
        for row in self.board:
            for piece in row:
                if piece is not None:
                    sign = 1 if piece.color == 'white' else -1
                    board_value += piece_values[type(piece).__name__] * sign
        if (self.is_checkmate('black')):
            board_value += 35
        elif (self.is_checkmate('white')):
            board_value -= 35
        else:
            if (self.is_check('black')):
                board_value += 2
            elif (self.is_check('white')):
                board_value -= 2
        return board_value

    def promote_pawn(self, pawn, promotion_piece):
        """
        Promote the given pawn to the specified promotion piece.
        """
        row, col = pawn.position
        self.board[row][col] = promotion_piece(pawn.position, pawn.color)

    def is_game_over(self):
        # Check for checkmate
        if self.is_checkmate(self.turn):
            # The current player is in checkmate, so the game is over
            return True

        # Check for stalemate (no valid moves for the current player)
        current_moves = self.get_all_possible_moves(self.turn)
        if not current_moves:
            return True

        return False
    
    def restart_game(self, chess_board):
        self.__init__(chess_board)