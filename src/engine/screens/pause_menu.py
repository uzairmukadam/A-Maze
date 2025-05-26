from src.engine.screens.menu import Menu

class PauseMenu(Menu):
    def __init__(self, window):
        options = [{"option": "Resume", "event": "resume"},
                   {"option": "Exit", "event": "exit"}]
        
        super().__init__(window, options)