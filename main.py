# main.py
import pygame
import sys
from chess_board import ChessBoard
from game_manager import GameManager
from dropdown import Dropdown

# Initialize Pygame
pygame.init()

# Game window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
BACKGROUND_COLOR = pygame.Color('white')
BAR_COLOR = pygame.Color('grey')
TEXT_COLOR = pygame.Color('black')
BUTTON_COLOR = pygame.Color('lightslategray')
BUTTON_HOVER_COLOR = pygame.Color('slategray')

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chess Game')

# Chess board and game manager
chess_board = ChessBoard()
game_manager = GameManager(chess_board)
game_manager.setup_board()

# Fonts
font = pygame.font.SysFont("Arial", 24)
button_font = pygame.font.SysFont("Arial", 18)

# Calculate board dimensions
board_height = chess_board.square_size * 8
top_bar_height = 50
bottom_bar_height = SCREEN_HEIGHT - board_height - top_bar_height

# Set up dropdown menu
dropdown_options = ["Player", "Computer - Easy", "Computer - Medium", "Computer - Hard", "Computer - Impossible"]
dropdown = Dropdown(10, 10, 200, 30, font, "Player", dropdown_options)

# Define button areas for undo and restart
undo_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - bottom_bar_height + 10, 70, 25)
restart_button_rect = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - bottom_bar_height + 10, 70, 25)

# Helper function to draw buttons with hover effect
def draw_button(button_rect, text, mouse_pos):
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    text_surf = button_font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

# Game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            dropdown.handle_event(event)
            if undo_button_rect.collidepoint(event.pos):
                game_manager.undo_move()
            elif restart_button_rect.collidepoint(event.pos):
                game_manager.restart_game(chess_board)
            elif not dropdown.show_options:
                adjusted_click_pos = (event.pos[0], event.pos[1])
                game_manager.handle_board_click(adjusted_click_pos, offset_y=top_bar_height)

    if game_manager.turn == 'black' and dropdown.selected_option.startswith("Computer"):
        # Call the negamax function to get the best move
        depth = 2  # Adjust the depth as needed
        alpha = float('-inf')
        beta = float('inf')
        result = game_manager.move_generator.negamax(game_manager, depth, alpha, beta, -1)
        print(result)
        if isinstance(result, tuple):
            best_move, _ = result
            piece, target_pos = best_move
            game_manager.move_piece(target_pos[0], target_pos[1], piece)


    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, BAR_COLOR, (0, 0, SCREEN_WIDTH, top_bar_height))
    pygame.draw.rect(screen, BAR_COLOR, (0, SCREEN_HEIGHT - bottom_bar_height, SCREEN_WIDTH, bottom_bar_height))
    chess_board.draw(screen, offset_y=top_bar_height)
    game_manager.highlight_valid_moves(screen, chess_board.square_size, offset_y=top_bar_height)
    game_manager.draw_pieces(screen, chess_board.square_size, offset_y=top_bar_height)
    game_manager.highlight_selected_square(screen, chess_board.square_size, offset_y=top_bar_height)
    dropdown.draw(screen)
    screen.blit(font.render("Player", True, TEXT_COLOR), (10, SCREEN_HEIGHT - bottom_bar_height + 15))

    elapsed_time = (pygame.time.get_ticks() - game_manager.start_ticks) // 1000
    time_left = max(game_manager.total_time - elapsed_time, 0)
    minutes, seconds = divmod(time_left, 60)
    screen.blit(font.render(f'Time: {minutes:02}:{seconds:02}', True, TEXT_COLOR), (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT - bottom_bar_height + 15))

    draw_button(undo_button_rect, "Undo", mouse_pos)
    draw_button(restart_button_rect, "Reset", mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()
