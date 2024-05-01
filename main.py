from game_manager import GameManager
from move_generator import MoveGenerator
import pygame
import sys
from chess_board import ChessBoard
from pygame_helpers import draw_text, draw_board_and_pieces, handle_board_click

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

# Players
white = 'p'
black = 'p'
depth = 2
num_processes = 3

# Chess board and game manager
game_manager = GameManager()
move_generator = MoveGenerator()
chess_board = ChessBoard()
game_manager.setup_board()

# Fonts
font = pygame.font.SysFont("Arial", 24)
button_font = pygame.font.SysFont("Arial", 18)

# Calculate board dimensions
board_height = chess_board.square_size * 8
top_bar_height = 50
bottom_bar_height = SCREEN_HEIGHT - board_height - top_bar_height

# Define solve button area
white_solve_button_rect = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - bottom_bar_height + 10, 125, 25)
black_solve_button_rect = pygame.Rect(SCREEN_WIDTH - 150, bottom_bar_height - 40, 125, 25)

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
            if undo_button_rect.collidepoint(event.pos):
                game_manager.undo_move()
            elif restart_button_rect.collidepoint(event.pos):
                game_manager.setup_board()
            elif white_solve_button_rect.collidepoint(event.pos):
                if white == 'p':
                    white = 'q'
                else:
                    white = 'p'
            elif black_solve_button_rect.collidepoint(event.pos):
                if black == 'p':
                    black = 'q'
                else:
                    black = 'p'
            else:
                if (white == 'p' and game_manager.turn == 'white') or (black == 'p' and game_manager.turn == 'black'):
                    adjusted_click_pos = (event.pos[0], event.pos[1])
                    handle_board_click(adjusted_click_pos, top_bar_height, chess_board.square_size, game_manager)
                elif white != 'p' and game_manager.turn == 'white':
                    result = move_generator.parallel_search(game_manager, depth, 1, num_processes)
                    if result == (float('-inf'), None):
                        print("Black Won The Game!")
                        game_manager.setup_board()
                        continue
                    print(result)
                    _, best_move = result
                    start_pos, target_pos = best_move
                    game_manager.make_move(start_pos, target_pos)
                elif black != 'p' and game_manager.turn == 'black':
                    result = move_generator.parallel_search(game_manager, depth, -1, num_processes)
                    if result == (float('inf'), None):
                        print("White Won The Game!")
                        game_manager.setup_board()
                        continue
                    print(result)
                    _, best_move = result
                    start_pos, target_pos = best_move
                    game_manager.make_move(start_pos, target_pos)


    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, BAR_COLOR, (0, 0, SCREEN_WIDTH, top_bar_height))
    pygame.draw.rect(screen, BAR_COLOR, (0, SCREEN_HEIGHT - bottom_bar_height, SCREEN_WIDTH, bottom_bar_height))
    chess_board.draw(screen, offset_y=top_bar_height)
    pieces = game_manager.get_pieces()
    draw_board_and_pieces(game_manager, screen, chess_board, chess_board.square_size, pieces, offset_y=top_bar_height)

    #player icons
    p1_txt = "Player 1 (White)" if white == 'p' else "Bot (White)"
    p2_txt = "Player 2 (Black)" if black == 'p' else "Bot (Black)"
    screen.blit(font.render(p1_txt, True, TEXT_COLOR), (10, SCREEN_HEIGHT - bottom_bar_height + 15))
    screen.blit(font.render(p2_txt, True, TEXT_COLOR), (10, bottom_bar_height - 40))

    draw_button(white_solve_button_rect, "Solve White", mouse_pos)
    draw_button(black_solve_button_rect, "Solve Black", mouse_pos)
    draw_button(undo_button_rect, "Undo", mouse_pos)
    draw_button(restart_button_rect, "Reset", mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()
