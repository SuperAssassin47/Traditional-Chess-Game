# Foundation for all menu systems
import pygame

class Button:
    def __init__(self, text, pos, size, font, idle_color, hover_color):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.font = font
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.idle_color
        pygame.draw.rect(screen, color, self.rect)

        font = pygame.font.Font(None, 32)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.hovered
