from src.engine.screens.menu import Menu

class MainMenu(Menu):
    def __init__(self, window):
        options = [
            {"option": "Start New Game", "event": "start_new_game"},
            {"option": "Load Map", "event": "load_map"},
            {"option": "Quit", "event": "quit_game"}
        ]
        super().__init__(window, options)

    def update(self, events):
        return super().update(events)
    
    def draw(self):
        return super().draw()