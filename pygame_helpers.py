import pygame

def draw_text(text, font, color, x, y, screen):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_board_and_pieces(game_manager, screen, chess_board, square_size, pieces, offset_y=0):
    chess_board.draw(screen, offset_y)
    if game_manager.selected_piece:
        notation = game_manager.selected_piece #0-63
        pos = game_manager.notation_to_pos(notation)
        x_selected = (pos % 8)
        y_selected = 7-(pos // 8)
        highlight_selected_color = (0, 255, 255)
        pygame.draw.rect(screen, highlight_selected_color, (x_selected * square_size, y_selected * square_size + offset_y, square_size, square_size))
        moves = game_manager.get_valid_moves(pos)
        valid_moves = []
        for move in moves:
            to_notation = game_manager.pos_to_notation(move)
            game_manager.make_move(notation, to_notation)
            if game_manager.is_check('white' if game_manager.turn != 'white' else 'black'):
                game_manager.undo_move()
                continue
            game_manager.undo_move()
            x_move = (move % 8)
            y_move = 7-(move // 8)
            pygame.draw.rect(screen, (255, 0, 0), (x_move * square_size, y_move * square_size + offset_y, square_size, square_size), 3)
    for piece in pieces:
        if piece:
            font = pygame.font.SysFont("Monospace", square_size)
            piece_image = font.render(piece.image, True, (0, 0, 0))
            x, y = piece.get_pygame_pos(square_size)
            screen.blit(piece_image, (x+15, y + offset_y))

def handle_board_click(click_pos, offset_y, square_size, game_manager):
    row = 7 - ((click_pos[1] - offset_y) // square_size)
    col = click_pos[0] // square_size
    pos = row * 8 + col
    if game_manager.selected_piece:
        if game_manager.selected_piece != game_manager.pos_to_notation(pos):
            game_manager.make_move(game_manager.selected_piece, game_manager.pos_to_notation(pos))
        game_manager.selected_piece = None
    else:
        if game_manager.get_piece_at_position(pos) != (None, None):
            game_manager.selected_piece = game_manager.pos_to_notation(pos)
