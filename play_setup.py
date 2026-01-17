import pygame
from buttons import Button
from game_state_base import GameState

class PlayState(GameState):
    def __init__(self):
        self.manager = manager
        self.font = pygame.font.SysFont("Arial", 20)
        self.selected_color = None
        self.selected_difficulty = None

    def enter(self):
        # player color choice for chess match
        self.white_button = Button("White", (150, 150), (200, 60), self.font, (200, 200, 200), (255, 255, 255))
        self.black_button = Button("Black", (150, 150), (200, 60), self.font, (200, 200, 200), (255, 255, 255))

        # difficulty buttons
        self.easy_btn = Button("Easy", (150, 250), (200, 60), self.font, (200, 200, 200), (255, 255, 255))
        self.medium_btn = Button("Medium", (350, 250), (200, 60), self.font, (200, 200, 200), (255, 255, 255))
        self.hard_btn = Button("Hard", (550, 250), (200, 60), self.font, (200, 200, 200), (255, 255, 255))

        # start match button
        self.start_btn = Button("Start Match", (300, 400), (200, 60), self.font, (200, 200, 200), (255, 255, 255))

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        buttons = [self.white_button, self.black_button, self.easy_btn, self.medium_btn, self.hard_btn]
        for button in buttons:
            button.update(mouse_pos)

        for event in events:
            if self.white_button.is_clicked(event):
                self.selected_color = "white"
            if self.black_button.is_clicked(event):
                self.selected_color = "black"
            if self.easy_btn.is_clicked(event):
                self.selected_difficulty = "easy"
            if self.medium_btn.is_clicked(event):
                self.selected_difficulty = "medium"
            if self.hard_btn.is_clicked(event):
                self.selected_color = "hard"

            if self.start_btn.is_clicked(event):
                self.manager.set_state("game")

    def render(self, screen):
        screen.fill((40, 40, 40))
        for button in [self.white_button, self.black_button, self.easy_btn, self.medium_btn, self.hard_btn]:
            button.draw(screen)
