from src.engine.screens.menu import Menu

class MainMenu(Menu):
    def __init__(self, window):
        options = [{"option": "Start Game", "event": "start_game"},
                   {"option": "Exit", "event": "quit"}]

        super().__init__(window, options)