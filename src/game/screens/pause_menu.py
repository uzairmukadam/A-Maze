from src.game.screens.menu import Menu

class PauseMenu(Menu):
    def __init__(self, window):
        options = [
            {"option": "Resume", "event": "resume"},
            {"option": "Return to Main Menu", "event": "main_menu"}
        ]
        super().__init__(window, options)
