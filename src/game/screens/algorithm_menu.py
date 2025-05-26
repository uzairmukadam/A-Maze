from src.engine.screens.menu import Menu

class AlgorithmMenu(Menu):
    def __init__(self, window):
        options = [{"option": "Predefined", "event": "predefined"},
                   {"option": "Back", "event": "back"}]
        
        super().__init__(window, options)