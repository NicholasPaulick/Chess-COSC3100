import pygame

class Dropdown:
    def __init__(self, x, y, width, height, font, main_option, options):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.main_option = main_option
        self.options = options
        self.show_options = False
        self.selected_option = main_option

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Draw border
        text_surf = self.font.render(self.selected_option, True, (0, 0, 0))
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

        if self.show_options:
            for i, option in enumerate(self.options, start=1):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + i*self.rect.height, self.rect.width, self.rect.height)
                pygame.draw.rect(screen, (255, 255, 255), option_rect)
                pygame.draw.rect(screen, (0, 0, 0), option_rect, 2)  # Option border
                option_text_surf = self.font.render(option, True, (0, 0, 0))
                screen.blit(option_text_surf, (option_rect.x + 5, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.show_options = not self.show_options
            else:
                for i, option in enumerate(self.options, start=1):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + i*self.rect.height, self.rect.width, self.rect.height)
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = option
                        self.show_options = False
                        break
