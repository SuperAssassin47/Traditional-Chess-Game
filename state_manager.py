from stats_screen import StatsScreen

class StateManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = {}
        self.current_state = None

    # add a new state
    def add_state(self, name, state):
        self.state[name] = state

    # set the current state
    def set_state(self, name, params=None):
        self.current_state = self.state[name]
        self.current_state.enter(params)

    # update the current state
    def update(self, events):
        if self.current_state:
            self.current_state.update(events)

    def render(self):
        if self.current_state:
            self.current_state.render(self.screen)