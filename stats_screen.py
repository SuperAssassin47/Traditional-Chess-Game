import pygame
from game_state_base import GameState

import pygame
from game_state_base import GameState
from buttons import Button

class StatsScreen(GameState):
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.Font(None, 60)
        self.button_font = pygame.font.Font(None, 40)

    def enter(self, params=None):
        # Create a real clickable Button object
        self.back_button = Button(
            "Main Menu",
            (200, 300),
            (250, 60),
            self.button_font,
            (200, 200, 200),
            (255, 255, 255)
        )

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)

        for event in events:
            if self.back_button.is_clicked(event):
                self.manager.set_state("main_menu")

    def render(self, screen):
        screen.fill((30, 30, 30))

        title = self.font.render("Statistics", True, (255, 255, 255))
        screen.blit(title, (200, 150))

        self.back_button.draw(screen)