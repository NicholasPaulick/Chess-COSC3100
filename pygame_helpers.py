import pygame

def draw_text(text, font, color, x, y, screen):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_board_and_pieces(screen, chess_board, square_size, pieces, offset_y=0):
    chess_board.draw(screen, offset_y)
    for piece in pieces:
        if piece:
            font = pygame.font.SysFont("Monospace", square_size)
            piece_image = font.render(piece.image, True, (0, 0, 0))
            x, y = piece.get_pygame_pos(square_size)
            screen.blit(piece_image, (x, y + offset_y))

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
