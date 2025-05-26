# src/engine/screens/main_menu.py
from src.engine.screens.menu import Menu
import pygame

class MainMenu(Menu):
    """
    Represents the main menu screen of the game.
    Inherits from the generic Menu class.
    """
    def __init__(self, window: pygame.Surface): # Removed config
        """
        Initializes the MainMenu.

        Args:
            window (pygame.Surface): The Pygame surface to draw on.
        """
        options = [{"option": "Start Game", "event": "start_game"},
                   {"option": "Settings", "event": "settings"},
                   {"option": "Exit", "event": "quit"}]

        super().__init__(window, options) # No config passed to super()