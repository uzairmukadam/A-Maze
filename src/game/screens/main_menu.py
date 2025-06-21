from src.game.screens.menu import Menu

class MainMenu(Menu):
    def __init__(self, window):
        options = [
            {"option": "Start Game", "event": "start_game"},
            {"option": "Quit", "event": "quit_game"}
        ]
        super().__init__(window, options)