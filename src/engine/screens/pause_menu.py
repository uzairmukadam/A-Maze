# src/engine/screens/pause_menu.py
from src.engine.screens.menu import Menu
import pygame

class PauseMenu(Menu):
    """
    Represents the pause menu screen of the game.
    Inherits from the generic Menu class.
    """
    def __init__(self, window: pygame.Surface): # Removed config
        """
        Initializes the PauseMenu.

        Args:
            window (pygame.Surface): The Pygame surface to draw on.
        """
        options = [{"option": "Resume", "event": "resume"},
                   {"option": "Return to Main Menu", "event": "exit"}]
        
        super().__init__(window, options) # No config passed to super()