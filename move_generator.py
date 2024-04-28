from chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King
import math
from collections import defaultdict

class MoveGenerator:
    def __init__(self, board):
        self.board = board
        self.move_tables = {
            Pawn: self._pawn_moves,
            Rook: self._rook_moves,
            Knight: self._knight_moves,
            Bishop: self._bishop_moves,
            Queen: self._queen_moves,
            King: self._king_moves,
        }

    def negamax(self, game_manager, depth, alpha, beta, color):
        # Check for game over conditions
        if depth == 0 or game_manager.is_game_over():
            evaluation = color * game_manager.evaluate_board()
            return evaluation, None

        text_color = 'black' if color == -1 else 'white'
        all_possible_moves = self.get_all_possible_moves(game_manager, text_color)

        if not all_possible_moves:
            evaluation = color * game_manager.evaluate_board()
            return evaluation, None

        max_eval = float('-inf')
        best_move = None
        for move in all_possible_moves:
            piece, target_pos = move
            original_position = piece.position
            game_manager.move_piece(target_pos[0], target_pos[1], piece)
            eval, _ = self.negamax(game_manager, depth - 1, -beta, -alpha, -color)  # always return eval and move
            game_manager.undo_move()
            piece.move(original_position)  # Restore the piece's position
            eval = -eval  # Negate eval since it's a minimizing move from the opponent's perspective

            if eval > max_eval:
                max_eval = eval
                best_move = move
                if max_eval >= beta:
                    break
            alpha = max(alpha, eval)  # Update alpha correctly based on negated evaluation
        return (max_eval, best_move)

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
            self._get_sliding_moves(row, col, d, moves, rook.color)

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
            self._get_sliding_moves(row, col, d, moves, bishop.color)

        return moves


    def _queen_moves(self, queen):
        moves = []
        # Combine directions for rook and bishop
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        row, col = queen.position  # Assuming each piece has a 'position' attribute
        for d in directions:
            self._get_sliding_moves(row, col, d, moves, queen.color)
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

    def _get_sliding_moves(self, row, col, direction, moves, color):
        """
        Helper function to get sliding moves for rooks, bishops, and queens.
        """
        dr, dc = direction
        for i in range(1, 8):
            new_row = row + dr * i
            new_col = col + dc * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
            else:
                break

    def get_all_possible_moves(self, game_manager, color):
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    moves = game_manager.get_moves(piece, game_manager.move_history[-1])
                    valid_moves = []
                    for move in moves:
                        original_pos = piece.position
                        game_manager.move_piece(move[0], move[1], piece)
                        if not game_manager.is_check(piece.color):
                            valid_moves.append((piece, move))
                        game_manager.undo_move()
                        piece.move(original_pos)  # Restore the piece's position
                    all_moves.extend(valid_moves)
        return all_moves