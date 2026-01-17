import pygame
import json
from game_state_base import GameState

class StateScreen(GameState):
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Arial", 20)

    def enter(self):
        try:
            with open("json/matches.json", "r") as f:
                self.data = json.load(f)
        except:
            data = []

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.set_state("main menu")
    def render(self, screen):
        screen.fill((20, 20, 20))
        y = 100

        total = len(self.data)
        wins = sum(1 for m in self.data if m["result"] == "win")
        losses = sum(1 for m in self.data if m["result"] == "loss")
        draws = sum(1 for m in self.data if m["result"] == "draw")

        stats = [
            f"Total Wins: {wins}",
            f"Total Losses: {losses}",
            f"Total Draws: {draws}",
            f"Total Games Played: {total}"
        ]

        for line in stats:
            surf = self.font.render(line, True, (255, 255, 255))
            screen.blit(surf, (50, y))
            y += 50
