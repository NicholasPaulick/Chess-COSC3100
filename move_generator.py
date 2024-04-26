from chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King
import math


class MoveGenerator:
    def __init__(self, board):
        self.board = board
        self.killer_moves = [(None, None), (None, None)]
        self.transposition_table = {}

    def negamax(self, game_manager, depth, alpha, beta, color):
        # Check if the current position is in the transposition table
        position_key = self.get_position_key(game_manager.board)
        if position_key in self.transposition_table:
            entry = self.transposition_table[position_key]
            if entry['depth'] >= depth and entry['turn'] == game_manager.turn:
                return entry['value']

        
        if depth == 0:
            return game_manager.evaluate_board()
    
        all_possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == game_manager.turn:
                    moves = game_manager.get_valid_moves(piece, None)
                    for move in moves:
                        all_possible_moves.append((piece, move))

        if not all_possible_moves:
            return color * game_manager.evaluate_board()
        
        # Order the moves based on the killer heuristic
        all_possible_moves = self.order_moves(all_possible_moves, game_manager.turn)

        max_eval = float('-inf')
        best_move = None
        for move in all_possible_moves:
            piece, target_pos = move
            original_pos = piece.position
            game_manager.execute_move(piece, target_pos)
            result = self.negamax(game_manager, depth - 1, -beta, -alpha, -color)
            game_manager.undo_move()
            if isinstance(result, tuple):
                _, eval = result
                eval = -eval
            else:
                eval = result
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        self.transposition_table[position_key] = {
            'value': (best_move, max_eval) if best_move else max_eval,
            'depth': depth,
            'turn': game_manager.turn
        }
        return (best_move, max_eval) if best_move else max_eval

    def order_moves(self, moves, turn):
        ordered_moves = []
        for move in moves:
            if move == self.killer_moves[0]:
                ordered_moves.insert(0, move)
            elif move == self.killer_moves[1]:
                ordered_moves.insert(1, move)
            else:
                ordered_moves.append(move)
        # Update the killer moves based on the current turn
        self.killer_moves[1] = self.killer_moves[0]
        self.killer_moves[0] = (None, None)
        return ordered_moves

    def get_position_key(self, board):
        # Generate a unique key for the current position
        key = ''.join(str(piece) for row in board for piece in row if piece)
        return key

    def _pawn_moves(self, pawn, last_move):
        moves = []
        row, col = pawn.position
        direction = -1 if pawn.color == 'white' else 1
        en_passant_row = 3 if pawn.color == 'white' else 4  # Row where pawn must be to capture en passant

        # Forward moves
        if self._is_empty((row + direction, col)):
            moves.append((row + direction, col))
            if (pawn.color == 'white' and row == 6) or (pawn.color == 'black' and row == 1) and self._is_empty((row + 2 * direction, col)):
                moves.append((row + 2 * direction, col))

        # Diagonal captures for en passant
        for dx in [-1, 1]:
            diag_pos = (row + direction, col + dx)
            if 0 <= diag_pos[1] < 8:  # Ensure it's on the board
                if self._is_opponent_piece(diag_pos, pawn.color):
                    moves.append(diag_pos)
                elif row == en_passant_row:  # Check if pawn is in correct row for en passant
                    if self._is_en_passant(pawn, (row, col + dx), last_move):
                        en_passant_capture_pos = (row + direction, col + dx)  # Square pawn moves to capture
                        moves.append(en_passant_capture_pos)
        return moves

    def _is_en_passant(self, pawn, target_pos, last_move):
        if not last_move:
            return False
        _, start_pos, end_pos, _, moved_piece_color = last_move
        # Check if the last moved piece was a pawn, it moved two squares vertically, and is adjacent to the current pawn's position
        if isinstance(last_move[0], Pawn) and moved_piece_color != pawn.color:
            # Correct row and the column is directly adjacent
            if abs(start_pos[0] - end_pos[0]) == 2 and end_pos[0] == pawn.position[0] and end_pos[1] == target_pos[1]:
                return True
        return False



    def _rook_moves(self, rook):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        row, col = rook.position

        for d in directions:
            for i in range(1, 8):  # Maximum board size in one direction
                new_row = row + d[0] * i
                new_col = col + d[1] * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check if within board bounds
                    if self.board[new_row][new_col] is None:  # Empty square
                        moves.append((new_row, new_col))
                    elif self.board[new_row][new_col].color != rook.color:  # Capture opponent's piece
                        moves.append((new_row, new_col))
                        break  # Can't move further in this direction
                    else:
                        break  # Blocked by a piece of the same color
                else:
                    break  # Off the board

        return moves


    def _knight_moves(self, knight):
        moves = []
        # Knight's movement options (L-shapes)
        move_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                        (1, -2), (1, 2), (2, -1), (2, 1)]

        row, col = knight.position  # Assuming each piece has a 'position' attribute

        for offset in move_offsets:
            new_row = row + offset[0]
            new_col = col + offset[1]

            # Check if the new position is within the board
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the new position is either empty or contains an opponent's piece
                target = self.board[new_row][new_col]
                if target is None or target.color != knight.color:
                    moves.append((new_row, new_col))

        return moves


    def _bishop_moves(self, bishop):
        moves = []
        # Diagonal movement directions: top-right, bottom-right, bottom-left, top-left
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        row, col = bishop.position  # Assuming each piece has a 'position' attribute

        for d in directions:
            for i in range(1, 8):  # The board is 8x8, so we limit the steps to 7 in any direction
                new_row = row + d[0] * i
                new_col = col + d[1] * i

                # Check if new position is off the board
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break  # Break if moving off the board
                
                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))  # Empty square is a valid move
                elif target.color != bishop.color:
                    moves.append((new_row, new_col))  # Capture opponent's piece
                    break  # Cannot move past this piece
                else:
                    break  # Blocked by a piece of the same color

        return moves


    def _queen_moves(self, queen):
        moves = []
        # Combine directions for rook and bishop
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

        row, col = queen.position  # Assuming each piece has a 'position' attribute

        for d in directions:
            for i in range(1, 8):
                new_row = row + d[0] * i
                new_col = col + d[1] * i

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target is None:
                        moves.append((new_row, new_col))
                    elif target.color != queen.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break

        return moves


    def _king_moves(self, king):
        moves = []
        # Directions: vertical, horizontal, and diagonal around the king
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

        row, col = king.position

        for d in directions:
            new_row = row + d[0]
            new_col = col + d[1]

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target is None or target.color != king.color:
                    moves.append((new_row, new_col))

        return moves

    def _is_empty(self, position):
        row, col = position
        return self.board[row][col] is None

    def _is_opponent_piece(self, position, color):
        row, col = position
        piece = self.board[row][col]
        return piece is not None and piece.color != color