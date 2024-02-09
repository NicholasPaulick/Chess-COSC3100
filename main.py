import pygame
import sys
from chess_board import ChessBoard
from game_manager import GameManager

# Initialize Pygame
pygame.init()

# Game window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chess Game')

# Chess board
chess_board = ChessBoard()

# Game manager
game_manager = GameManager()
game_manager.setup_board()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Convert mouse position to board coordinates
            pos = pygame.mouse.get_pos()
            row = pos[1] // chess_board.square_size
            col = pos[0] // chess_board.square_size
            if game_manager.selected_piece:
                game_manager.move_piece(row, col)
            else:
                game_manager.select_piece(row, col)
    
    # Drawing
    screen.fill(BACKGROUND_COLOR)
    chess_board.draw(screen)
    game_manager.highlight_selected_square(screen, chess_board.square_size)
    game_manager.draw_pieces(screen, chess_board.square_size)

    pygame.display.flip()

pygame.quit()
sys.exit()
