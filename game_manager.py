import chess_pieces

class GameManager:
    def __init__(self):
        # Bitboards for each piece type and color
        # white
        self.white_pawns = 0b0000000000000000000000000000000000000000000000001111111100000000
        self.white_rooks = 0b0000000000000000000000000000000000000000000000000000000010000001
        self.white_knights = 0b0000000000000000000000000000000000000000000000000000000001000010
        self.white_bishops = 0b0000000000000000000000000000000000000000000000000000000000100100
        self.white_queens = 0b0000000000000000000000000000000000000000000000000000000000001000
        self.white_kings = 0b0000000000000000000000000000000000000000000000000000000000010000
        # black
        self.black_pawns = 0b0000000011111111000000000000000000000000000000000000000000000000
        self.black_rooks = 0b1000000100000000000000000000000000000000000000000000000000000000
        self.black_knights = 0b0100001000000000000000000000000000000000000000000000000000000000
        self.black_bishops = 0b0010010000000000000000000000000000000000000000000000000000000000
        self.black_queens = 0b0000100000000000000000000000000000000000000000000000000000000000
        self.black_kings = 0b0001000000000000000000000000000000000000000000000000000000000000

        self.selected_piece = None
        self.valid_moves = []
        self.move_history = []
        self.turn = 'white'

    def setup_board(self):
        # Reset the board to the initial state
        self.__init__()

    def make_move(self, from_notation, to_notation):
        from_pos = self.notation_to_pos(from_notation)
        to_pos = self.notation_to_pos(to_notation)

        # Simplified move logic, assuming existing conditions are met
        piece_moved, moved_color = self.get_piece_at_position(from_pos)
        piece_captured, captured_color = self.get_piece_at_position(to_pos)

        # Record the move history
        move_details = {
            'move': self.get_piece_at_position(from_pos),
            'from_pos': from_pos,
            'to_pos': to_pos,
            'captured': self.get_piece_at_position(to_pos)
        }
        self.move_history.append(move_details)

        # Captures
        if piece_captured:
            self.update_bitboard(to_pos, piece_captured, captured_color, remove=True)
        
        # Remove the piece from the original position
        self.update_bitboard(from_pos, piece_moved, moved_color, remove=True)
        # Add the piece to the new position
        self.update_bitboard(to_pos, piece_moved, moved_color, remove=False)
        
        # Switch turns
        self.turn = 'black' if self.turn == 'white' else 'white'

    def undo_move(self):
        if not self.move_history:
            return  # No move to undo

        last_move = self.move_history.pop()
        piece_moved, moved_color = last_move['move']
        from_pos = last_move['from_pos']
        to_pos = last_move['to_pos']
        piece_captured, captured_color = last_move['captured']
        
        # Move the piece back
        self.update_bitboard(to_pos, piece_moved, moved_color, remove=True)
        self.update_bitboard(from_pos, piece_moved, moved_color, remove=False)
        
        # Restore the captured piece
        if piece_captured:
            self.update_bitboard(to_pos, piece_captured, captured_color, remove=False)

        # Switch turns back
        self.turn = 'black' if self.turn == 'white' else 'white'

    def get_valid_moves(self, pos):
        # This is a simplified placeholder for generating moves
        piece, piece_color = self.get_piece_at_position(pos)
        valid_moves = []
        match piece:
            case 'pawns':
                valid_moves.extend(self.pawn_moves(pos, piece_color))
            case 'rooks':
                valid_moves.extend(self.rook_moves(pos, piece_color))
            case 'knights':
                valid_moves.extend(self.knight_moves(pos, piece_color))
            case 'bishops':
                valid_moves.extend(self.bishop_moves(pos, piece_color))
            case 'queens':
                valid_moves.extend(self.queen_moves(pos, piece_color))
            case 'kings':
                valid_moves.extend(self.king_moves(pos, piece_color))
        # Add other pieces move logic here
        return valid_moves

    def update_bitboard(self, pos, piece_type, color, remove=False):
        if piece_type is None or color is None:
            return

        bit = 1 << pos
        board = getattr(self, f"{color}_{piece_type}")
        if remove:
            board &= ~bit  # Remove the piece
        else:
            board |= bit  # Place the piece
        setattr(self, f"{color}_{piece_type}", board)

    def get_piece_at_position(self, pos):
        if type(pos) != int:
            return None, None
        mask = 1 << pos
        for color in ['white', 'black']:
            for piece_type in ['pawns', 'rooks', 'knights', 'bishops', 'queens', 'kings']:
                if getattr(self, f"{color}_{piece_type}") & mask:
                    return piece_type, color
        return None, None

    # Check and moves
    def is_check(self, color):
        king_pos = self.find_king(color)
        opposing_color = 'black' if color == 'white' else 'white'
        for start_pos, end_pos in self.get_all_moves(opposing_color):
            if king_pos in end_pos:
                return True
        return False

    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
        # Get all moves for the current player
        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece and color == color:
                if self.get_valid_moves(pos):
                    return False
        return true

    def find_king(self, color):
        king_bitboard = self.white_kings if color == 'white' else self.black_kings
        # Return the position of the king
        return (king_bitboard & -king_bitboard).bit_length() - 1

    def get_all_moves(self, color):
        moves = []
        for pos in range(64):
            piece, piece_color = self.get_piece_at_position(pos)
            if piece and (color == piece_color):
                valid_moves = self.get_valid_moves(pos)
                if valid_moves:
                    moves.append((pos, valid_moves))
        return moves


    # Evaluation
    def evaluate_board(self):
        score = 0
        is_ahead = self.check_if_ahead()

        material_value = self.evaluate_material()

        pawn_structure_score = self.evaluate_pawn_structure() * (1.5 if is_ahead else 1)
        king_safety_score = self.evaluate_king_safety() * (1.2 if not is_ahead else 1.5)
        center_control_score = self.evaluate_center_control() * (1.5 if not is_ahead else 1)
        mobility_score = self.evaluate_mobility() * (0.3 if not is_ahead else 0.1)
        tactics_score = self.evaluate_tactics() * (0.8 if not is_ahead else 0.3)
        coordination_score = self.evaluate_coordination() * (0.2 if not is_ahead else 0.1)
        development_score = self.evaluate_development() * (0.7 if not is_ahead else 0.3)
        advanced_king_safety_score = self.evaluate_advanced_king_safety() * (0.5 if not is_ahead else 1)
        pawn_chains_blocks_score = self.evaluate_pawn_chains_and_blocks() * (0.4 if not is_ahead else 0.2)

        # Check for checkmate
        if self.is_checkmate('white'):
            return -200000
        elif self.is_checkmate('black'):
            return 200000

        # Incorporate other factors
        if self.turn == 'white':
            score += (material_value + pawn_structure_score + king_safety_score + center_control_score + mobility_score + tactics_score + coordination_score + development_score + advanced_king_safety_score + pawn_chains_blocks_score)
        else:
            score -= (material_value + pawn_structure_score + king_safety_score + center_control_score + mobility_score + tactics_score + coordination_score + development_score + advanced_king_safety_score + pawn_chains_blocks_score)
        return score

    def evaluate_material(self):
        piece_values = {'pawns': 1, 'knights': 3, 'bishops': 3.5, 'rooks': 5, 'queens': 9, 'kings': 200}
        score = 0
        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece:
                score += piece_values[piece] if color == self.turn else -piece_values[piece]
        return score

    def check_if_ahead(self):
        # Check if the engine is significantly ahead in material or position
        material_difference = self.evaluate_material()
        return material_difference > 8

    def evaluate_tactics(self):
        score = 0
        # This is a simple implementation idea; more detailed checking based on actual piece moves is needed
        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece and (piece == 'knights' or piece == 'queens'):
                moves = self.get_valid_moves(pos)
                if len(moves) >= 2:  # A very simplistic way to check for potential forks
                    # Check if multiple captures are possible
                    capture_moves = [move for move in moves if self.get_piece_at_position(move)]
                    if len(capture_moves) > 1:
                        if color == 'white':
                            score += 3  # Adding a simple bonus for potential forks
                        else:
                            score -= 3
        return score

    def evaluate_coordination(self):
        score = 0
        # Check for bishops on long diagonals, rooks on open files, etc.
        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece and piece == 'bishops':
                moves = self.get_valid_moves(pos)
                if len(moves) > 4:  # Simplistic check for bishop effectiveness
                    if color == 'white':
                        score += 1
                    else:
                        score -= 1
        return score

    def evaluate_development(self):
        score = 0
        early_game = len(self.move_history) < 20  # Adjust as needed for the early game definition
        undeveloped_pieces = {'rooks': 2, 'knights': 3, 'bishops': 3}  # Penalty values for undeveloped pieces

        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece in undeveloped_pieces:
                if early_game and not self.piece_has_moved(pos):
                    score += undeveloped_pieces[piece] if color == 'white' else -undeveloped_pieces[piece]

        return score

    def piece_has_moved(self, pos):
        # Simple check if a piece has moved, based on its current position vs initial position
        return pos in [self.move_history[i]['from_pos'] for i in range(len(self.move_history))]

    def evaluate_advanced_king_safety(self):
        score = 0
        # Assuming we already have methods to determine open files or dangerous diagonals
        for color in ['white', 'black']:
            king_pos = self.find_king(color)
            if self.is_file_open(king_pos) or self.is_diagonal_open(king_pos):
                score -= 5 if color == 'white' else 5  # Adding a penalty for king exposure

        return score

    def is_file_open(self, pos):
        file = pos % 8
        file_mask = 0x0101010101010101 << file  # Bit mask for the file
        return not (self.white_pawns & file_mask) and not (self.black_pawns & file_mask)

    def is_diagonal_open(self, pos):
        # Simplistic check; should be refined based on actual diagonal threats
        return False  # Placeholder for diagonal checks

    def evaluate_pawn_chains_and_blocks(self):
        score = 0
        # Pawn chains and blocked pawns
        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece == 'pawns':
                if self.is_pawn_in_chain(pos, color):
                    score += 1 if color == 'white' else -1
                if self.is_pawn_blocked(pos, color):
                    score -= 1 if color == 'white' else 1

        return score

    def is_pawn_in_chain(self, pos, color):
        # Check if a pawn is protected by another pawn
        if color == 'white' and pos < 56:
            return bool(self.white_pawns & (1 << (pos + 9))) or bool(self.white_pawns & (1 << (pos + 7)))
        elif color == 'black' and pos > 7:
            return bool(self.black_pawns & (1 << (pos - 9))) or bool(self.black_pawns & (1 << (pos - 7)))
        return False

    def is_pawn_blocked(self, pos, color):
        # Check if a pawn is blocked directly in front
        if color == 'white' and pos < 56:
            return bool(self.black_pawns & (1 << (pos + 8)))
        elif color == 'black' and pos > 7:
            return bool(self.white_pawns & (1 << (pos - 8)))
        return False

    def evaluate_pawn_structure(self):
        score = 0
        isolated_penalty = 0
        doubled_penalty = -1
        backward_penalty = 0
        passed_pawn_bonus = 2

        # Evaluate white pawns
        for pos in range(64):
            mask = 1 << pos
            if self.white_pawns & mask:
                isolated = self.is_pawn_isolated(pos, 'white')
                doubled = self.is_pawn_doubled(pos, 'white')
                backward = self.is_pawn_backward(pos, 'white')
                passed = self.is_pawn_passed(pos, 'white')

                score += isolated * isolated_penalty
                score += doubled * doubled_penalty
                score += backward * backward_penalty
                score += passed * passed_pawn_bonus

        # Evaluate black pawns
        for pos in range(64):
            mask = 1 << pos
            if self.black_pawns & mask:
                isolated = self.is_pawn_isolated(pos, 'black')
                doubled = self.is_pawn_doubled(pos, 'black')
                backward = self.is_pawn_backward(pos, 'black')
                passed = self.is_pawn_passed(pos, 'black')

                score -= isolated * isolated_penalty
                score -= doubled * doubled_penalty
                score -= backward * backward_penalty
                score -= passed * passed_pawn_bonus

        return score

    def evaluate_king_safety(self):
        score = 0
        pawn_shield_bonus = 1

        # Evaluate white king
        white_king_pos = self.find_king('white')
        has_pawn_shield = self.has_pawn_shield(white_king_pos, 'white')
        score += has_pawn_shield * pawn_shield_bonus

        # Evaluate black king
        black_king_pos = self.find_king('black')
        has_pawn_shield = self.has_pawn_shield(black_king_pos, 'black')
        score -= has_pawn_shield * pawn_shield_bonus

        return score

    def evaluate_center_control(self):
        score = 0
        center_squares = [27, 28, 35, 36]
        center_control_weight = 2

        # Evaluate white pieces
        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece and color == 'white':
                if pos in center_squares:
                    score += center_control_weight

        # Evaluate black pieces
        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece and color == 'black':
                if pos in center_squares:
                    score -= center_control_weight

        return score

    def evaluate_mobility(self):
        score = 0
        for pos in range(64):
            piece, color = self.get_piece_at_position(pos)
            if piece and color == 'white':
                score += len(self.get_valid_moves(pos))
            elif piece and color == 'black':
                score -= len(self.get_valid_moves(pos))
        return score

    def is_pawn_isolated(self, pos, color):
        rank, file = pos // 8, pos % 8
        if color == 'white':
            file_mask_left = self.white_pawns >> (file if file > 0 else 0)
            file_mask_right = self.white_pawns << (7 - file if file < 7 else 0)
        else:
            file_mask_left = self.black_pawns >> (file if file > 0 else 0)
            file_mask_right = self.black_pawns << (7 - file if file < 7 else 0)

        mask_left = file_mask_left & (1 << pos)
        mask_right = file_mask_right & (1 << pos)
        return not (mask_left or mask_right)

    def is_pawn_doubled(self, pos, color):
        rank, file = pos // 8, pos % 8
        if color == 'white':
            file_mask = self.white_pawns & (0xFF << (file * 8))
        else:
            file_mask = self.black_pawns & (0xFF << (file * 8))
        return bin(file_mask).count('1') > 1

    def is_pawn_backward(self, pos, color):
        rank, file = pos // 8, pos % 8
        if color == 'white':
            if rank == 0 or rank == 7:
                return False
            front_mask = self.white_pawns >> 8
            return not front_mask & (1 << (pos - 8))
        else:
            if rank == 0 or rank == 7:
                return False
            front_mask = self.black_pawns << 8
            return not front_mask & (1 << (pos + 8))

    def is_pawn_passed(self, pos, color):
        rank, file = pos // 8, pos % 8
        if color == 'white':
            front_mask = self.white_pawns >> 8
            if rank == 7:
                return True
            while rank < 7:
                rank += 1
                front_mask >>= 8
                if front_mask & (1 << pos):
                    return False
            return True
        else:
            front_mask = self.black_pawns << 8
            if rank == 0:
                return True
            while rank > 0:
                rank -= 1
                front_mask <<= 8
                if front_mask & (1 << pos):
                    return False
            return True

    def has_pawn_shield(self, king_pos, color):
        if color == 'white':
            pawn_bitboard = self.white_pawns
        else:
            pawn_bitboard = self.black_pawns

        pawn_shield_masks = [
            pawn_bitboard >> 7, pawn_bitboard >> 8, pawn_bitboard >> 9,
            pawn_bitboard << 7, pawn_bitboard << 9
        ]
        return any(mask & (1 << king_pos) for mask in pawn_shield_masks)

    # View Board
    def print_board(self):
        # Print a visual representation of the board
        for row in range(8):
            print(" ".join(self.get_piece_symbol((7-row)*8 + col) for col in range(8)))

    def get_piece_symbol(self, pos):
        # Helper function to get a symbol for a piece at a given position
        mask = 1 << pos
        # white
        if self.white_pawns & mask: return '♙'
        if self.white_rooks & mask: return '♖'
        if self.white_bishops & mask: return '♗'
        if self.white_knights & mask: return '♘'
        if self.white_queens & mask: return '♕'
        if self.white_kings & mask: return '♔'
        # black
        if self.black_pawns & mask: return '♟'
        if self.black_rooks & mask: return '♜'
        if self.black_bishops & mask: return '♝'
        if self.black_knights & mask: return '♞'
        if self.black_queens & mask: return '♛'
        if self.black_kings & mask: return '♚'
        # Add symbols for other pieces
        return '.'

    # Piece Moves
    def pawn_moves(self, pos, piece_color):
        direction = 8 if piece_color == 'white' else -8
        start_row = 1 if piece_color == 'white' else 6
        moves = []

        # Single move forward
        if not self.get_piece_at_position(pos + direction)[0]:
            moves.append(pos + direction)
            # Double move forward
            if (piece_color == 'white' and pos // 8 == 1) or (piece_color == 'black' and pos // 8 == 6):
                if not self.get_piece_at_position(pos + 2 * direction)[0]:
                    moves.append(pos + 2 * direction)

        # Captures
        for offset in [-1, 1]:
            capture_pos = pos + direction + offset
            if not (0 <= capture_pos < 64):
                break
            # Check wrapping
            if abs((pos // 8) - (capture_pos // 8)) != 1:
                break
            captured_piece, captured_color = self.get_piece_at_position(capture_pos)
            if captured_piece and captured_color != piece_color:
                moves.append(capture_pos)

        return moves

    def rook_moves(self, pos, piece_color):
        moves = []
        directions = [-8, 8, -1, 1]  # up, down, left, right
        for direction in directions:
            for i in range(1, 8):
                next_pos = pos + i * direction
                if not (0 <= next_pos < 64):
                    break
                if direction in [-1, 1] and (pos // 8) != (next_pos // 8):
                    break
                elif direction in [-8, 8] and (pos % 8) != (next_pos % 8):
                    break

                captured_piece, captured_color = self.get_piece_at_position(next_pos)
                if captured_piece:
                    if captured_color != piece_color:
                        moves.append(next_pos)
                    break
                moves.append(next_pos)
        return moves

    def bishop_moves(self, pos, piece_color):
        moves = []
        directions = [-9, -7, 7, 9]  # diagonal movements
        for direction in directions:
            for i in range(1, 8):  # can potentially move up to 7 squares
                next_pos = pos + i * direction
                if not (0 <= next_pos < 64):
                    break
                # Check wrapping
                if abs((pos // 8) - (next_pos // 8)) != i:
                    break

                captured_piece, captured_color = self.get_piece_at_position(next_pos)
                if captured_piece:
                    if captured_color != piece_color:
                        moves.append(next_pos)
                    break
                moves.append(next_pos)
        return moves

    def queen_moves(self, pos, piece_color):
        # Combine rook and bishop moves
        return self.rook_moves(pos, piece_color) + self.bishop_moves(pos, piece_color)

    def knight_moves(self, pos, piece_color):
        moves = []
        knight_offsets = [-17, -15, -10, -6, 6, 10, 15, 17]

        for offset in knight_offsets:
            next_pos = pos + offset

            if not (0 <= next_pos < 64):
                continue

            # Calculate current and next row and column
            current_row, current_col = pos // 8, pos % 8
            next_row, next_col = next_pos // 8, next_pos % 8

            # Check if the move is a valid knight move
            if abs(current_row - next_row) == 2 and abs(current_col - next_col) == 1 or \
               abs(current_row - next_row) == 1 and abs(current_col - next_col) == 2:
                captured_piece, captured_color = self.get_piece_at_position(next_pos)

                if not captured_piece or (captured_piece and captured_color != piece_color):
                    moves.append(next_pos)

        return moves

    def king_moves(self, pos, piece_color):
        moves = []
        king_offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
        for offset in king_offsets:
            next_pos = pos + offset
            if 0 <= next_pos < 64:
                if (pos % 8 == 0 and offset in [-9, -1, 7]) or \
                   (pos % 8 == 7 and offset in [-7, 1, 9]) or \
                   (pos // 8 == 0 and offset in [-9, -7, -8]) or \
                   (pos // 8 == 7 and offset in [7, 8, 9]):
                    continue
                captured_piece, captured_color = self.get_piece_at_position(next_pos)
                if not captured_piece or captured_color != piece_color:
                    moves.append(next_pos)

        # Castling logic remains the same
        # Add basic castling logic (not considering check or other castling conditions)
        if piece_color == 'white':
            # Kingside castling
            if self.white_kings == (1 << 4) and self.white_rooks & (1 << 7):
                if all(not self.get_piece_at_position(i)[0] for i in [5, 6]):
                    moves.append(6)  # Add kingside castling move
            # Queenside castling
            if self.white_kings == (1 << 4) and self.white_rooks & (1):
                if all(not self.get_piece_at_position(i)[0] for i in [1, 2, 3]):
                    moves.append(2)  # Add queenside castling move
        elif piece_color == 'black':
            # Kingside castling
            if self.black_kings == (1 << 60) and self.black_rooks & (1 << 63):
                if all(not self.get_piece_at_position(i)[0] for i in [61, 62]):
                    moves.append(62)
            # Queenside castling
            if self.black_kings == (1 << 60) and self.black_rooks & (1 << 56):
                if all(not self.get_piece_at_position(i)[0] for i in [57, 58, 59]):
                    moves.append(58)
        return moves

    # Notation
    def user_move(self):
        from_notation = input("Enter the starting position of the piece (e.g., 'e2'): ")
        if from_notation == 'u':
            self.undo_move()
            self.undo_move()
        else:
            valid_moves = self.get_valid_moves(self.notation_to_pos(from_notation))
            print(" ".join(self.pos_to_notation(move) for move in valid_moves))
            to_notation = input("Enter the destination position (e.g., 'e4'): ")
            self.make_move(from_notation, to_notation)
            print("Moved from", from_notation, "to", to_notation)

    def pos_to_notation(self, pos):
        """Converts a board position index (0-63) to algebraic notation ('a1' to 'h8')."""
        file = chr((pos % 8) + ord('a'))  # Calculate file (column)
        rank = str((pos // 8) + 1)  # Calculate rank (row)
        return file + rank

    def notation_to_pos(self, notation):
        """Converts algebraic notation ('a1' to 'h8') to a board position index (0-63)."""
        file = ord(notation[0]) - ord('a')  # Convert file (column) from letter to number
        rank = int(notation[1]) - 1  # Convert rank (row) to zero-based index
        return rank * 8 + file

    def get_pieces(self):
        pieces = []
        for pos in reversed(range(64)):
            piece, color = self.get_piece_at_position(pos)
            if piece:
                piece_class_name = piece.capitalize().strip('s')
                piece_class = getattr(chess_pieces, piece_class_name)
                if color == 'white':
                    pieces.append(piece_class((pos // 8, pos % 8), 'white'))
                else:
                    pieces.append(piece_class((pos // 8, pos % 8), 'black'))
        return pieces
