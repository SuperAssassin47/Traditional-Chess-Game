import pygame
from state_manager import StateManager
from main_menu_screen import MainMenu
from game_state import Game, ResultScreen
from stats_screen import StatsScreen

window_width = 800
window_height = 500

def main():
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption("Traditional Chess Game")

    manager = StateManager(screen)

    # state registration
    manager.add_state("main_menu", MainMenu(manager))
    manager.add_state("game", Game(manager))
    manager.add_state("result_screen", ResultScreen(manager))
    manager.add_state("stats_screen", StatsScreen(manager))

    # start the main menu system
    manager.set_state("main_menu")

    # the main application loop
    running = True
    clock = pygame.time.Clock()

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        manager.update(events)
        manager.render()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
