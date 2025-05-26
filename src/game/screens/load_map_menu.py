from src.engine.screens.menu import Menu

class LoadMapMenu(Menu):
    def __init__(self, window):
        options = [{"option": "Map", "event": "map_1"},
                   {"option": "Back", "event": "back"}]
        
        super().__init__(window, options)