# src/engine/screens/main_menu.py
from src.engine.screens.menu import Menu

class PauseMenu(Menu):
    def __init__(self, window):
        options = [
            {"option": "Resume", "event": "resume"},
            {"option": "Return to Main Menu", "event": "main_menu"}
        ]
        super().__init__(window, options)

    def update(self, events):
        return super().update(events)
    
    def draw(self):
        return super().draw()