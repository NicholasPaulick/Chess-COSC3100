import multiprocessing
import math
import numpy as np
import random
from copy import deepcopy

class MoveGenerator:
    def parallel_search(self, game_manager, depth, color, num_processes):
        pool = multiprocessing.Pool(processes=num_processes)
        alpha = -float('inf')
        beta = float('inf')

        text_color = 'black' if color == -1 else 'white'

        if game_manager.is_checkmate(text_color):
            return -float('inf'), None

        all_possible_moves = game_manager.get_all_moves(text_color)
        all_possible_moves.reverse()
        num_moves = len(all_possible_moves)
        chunksize = num_moves // num_processes
        remainder = num_moves % num_processes
        tasks = []

        start = 0
        for i in range(num_processes):
            end = start + chunksize + (1 if i < remainder else 0)  # Distribute remainder among the first few processes
            partial_moves = all_possible_moves[start:end]
            partial_moves.reverse()
            tasks.append((deepcopy(game_manager), depth, alpha, beta, color, partial_moves))
            start = end

        results = pool.map(self.process_chunk, tasks)
        pool.close()
        pool.terminate()
        pool.join()

        print(results)

        best_move = None
        if text_color == 'white':
            max_eval = float('-inf')
            for eval, move in results:
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
        else:
            max_eval = float('inf')
            for eval, move in results:
                if eval < max_eval:
                    max_eval = eval
                    best_move = move
        return max_eval, best_move

    def process_chunk(self, args):
        game_manager, depth, alpha, beta, color, moves = args
        best_move = None
        text_color = 'black' if color == -1 else 'white'
        if text_color == 'white':
            max_eval = float('-inf')
        else:
            max_eval = float('inf')
    
        for start_pos, valid_moves in moves:
            start_notation = game_manager.pos_to_notation(start_pos)
            for end_pos in valid_moves:
                end_notation = game_manager.pos_to_notation(end_pos)
                game_manager.make_move(start_notation, end_notation)
                if game_manager.is_check(text_color):
                    game_manager.undo_move()
                    continue
                eval, _ = self.negamax(game_manager, depth-1, -beta, -alpha, -color)
                game_manager.undo_move()
                
                if text_color == 'white':
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (start_notation, end_notation)
                    alpha = max(alpha, eval)
                    if alpha >= beta:
                        break
                else:
                    if eval < max_eval:
                        max_eval = eval
                        best_move = (start_notation, end_notation)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return (max_eval, best_move)
            

    def negamax(self, game_manager, depth, alpha, beta, color):
        # Check for game over conditions
        if depth == 0:
            evaluation = color * game_manager.evaluate_board()
            return evaluation, None

        text_color = 'black' if color == -1 else 'white'

        if game_manager.is_checkmate(text_color):
            return -float('inf'), None

        rng = np.random.default_rng()
        all_possible_moves = game_manager.get_all_moves(text_color)
        random.seed(math.pow(len(all_possible_moves), rng.integers(low=0, high=100)))
        random.shuffle(all_possible_moves)

        if not all_possible_moves:
            evaluation = color * game_manager.evaluate_board()
            return evaluation, None

        if text_color == 'white':
            max_eval = float('-inf')
        else:
            max_eval = float('inf')
        best_move = None

        for start_pos, valid_moves in all_possible_moves:
            start_notation = game_manager.pos_to_notation(start_pos)
            for end_pos in valid_moves:
                end_notation = game_manager.pos_to_notation(end_pos)
                game_manager.make_move(start_notation, end_notation)
                if game_manager.is_check(text_color):
                    game_manager.undo_move()
                    continue  # Skip moves that leave the king in check

                eval, _ = self.negamax(game_manager, depth - 1, -beta, -alpha, -color)
                game_manager.undo_move()

                if text_color == 'white':
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (start_notation, end_notation)
                    alpha = max(alpha, eval)
                    if alpha >= beta:
                        break
                else:
                    if eval < max_eval:
                        max_eval = eval
                        best_move = (start_notation, end_notation)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return (max_eval, best_move)