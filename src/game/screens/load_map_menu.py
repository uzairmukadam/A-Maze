# src/game/screens/load_map_menu.py
import pygame
from src.engine.screens.menu import Menu

class LoadMapMenu(Menu):
    """
    Represents the load map menu where players can select a predefined map.
    Inherits from the generic Menu class.
    """
    def __init__(self, window: pygame.Surface, config: dict):
        """
        Initializes the LoadMapMenu.

        Args:
            window (pygame.Surface): The Pygame surface to draw on.
            config (dict): The game configuration dictionary.
                           (Note: config is now passed to GameLogic/Player,
                           not used directly by Menu base class for its constants).
        """
        options = [
            {"option": "Map 1", "event": "map_1"},
            # {"option": "Map 2", "event": "map_2"}, # Future
            {"option": "Back", "event": "back"}
        ]
        
        # --- FIX ---
        # Removed 'config' from the super().__init__() call
        super().__init__(window, options)
        # -------------

        # If you need to store config for other methods in LoadMapMenu specific logic,
        # you would do:
        # self.config = config