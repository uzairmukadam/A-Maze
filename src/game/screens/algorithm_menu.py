# src/game/screens/algorithm_menu.py
import pygame
from src.engine.screens.menu import Menu

class AlgorithmMenu(Menu):
    """
    Represents the algorithm selection menu.
    Inherits from the generic Menu class.
    """
    def __init__(self, window: pygame.Surface, config: dict):
        """
        Initializes the AlgorithmMenu.

        Args:
            window (pygame.Surface): The Pygame surface to draw on.
            config (dict): The game configuration dictionary.
                           (Note: config is now passed to GameLogic/Player,
                           not used directly by Menu base class for its constants).
        """
        options = [
            {"option": "Predefined Maze", "event": "predefined"},
            # {"option": "DFS Generator", "event": "dfs_generator"}, # Future
            # {"option": "Prim's Algorithm", "event": "prims_algorithm"}, # Future
            {"option": "Back", "event": "back"}
        ]
        
        # --- FIX ---
        # Removed 'config' from the super().__init__() call
        super().__init__(window, options) 
        # -------------

        # If you need to store config for other methods in AlgorithmMenu specific logic
        # (which is not currently the case based on your code), you would do:
        # self.config = config