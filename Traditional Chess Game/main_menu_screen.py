import pygame
from buttons import Button
from game_state_base import GameState

class MainMenu(GameState):
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Arial", 20)

    def enter(self, params=None):
        self.play = Button("Play", (300, 200), (200, 60), self.font, (200, 200, 200), (255, 255, 255))
        self.stats = Button("Statistics", (300, 300), (200, 60), self.font, (200, 200, 200), (255, 255, 255))
        self.quit = Button("Quit", (300, 400), (200, 60), self.font, (200, 200, 200), (255, 255, 255))

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for button in [self.play, self.stats, self.quit]:
            button.update(mouse_pos)

        for event in events:
            if self.play.is_clicked(event):
                self.manager.set_state("game") # start the chess match
            if self.stats.is_clicked(event):
                self.manager.set_state("stats_screen")
            if self.quit.is_clicked(event):
                pygame.quit()
                raise SystemExit

    def render(self, screen):
        screen.fill((0, 0, 0))
        for button in [self.play, self.stats, self.quit]:
            button.draw(screen)
