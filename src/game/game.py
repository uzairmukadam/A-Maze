# src/game/game.py
import pygame

from src.game.screens.algorithm_menu import AlgorithmMenu
from src.game.screens.load_map_menu import LoadMapMenu

from src.game.maze_generator.predefined import Predefined

from src.game.game_logic.game_logic import GameLogic


class GameState:
    """
    Defines the states within the main game module (not the engine).
    """
    ALGORITHM_MENU = "algorithm_menu"
    LOAD_MAP = "load_map"
    GAMEPLAY = "gameplay"
    GAME_OVER = "game_over"


class Game:
    """
    Manages the overall game flow, including maze selection, gameplay,
    and transitions between game-specific screens.
    """
    def __init__(self, window: pygame.Surface, config: dict, load_map_directly: bool = False):
        """
        Initializes the Game module.

        Args:
            window (pygame.Surface): The Pygame surface to draw game elements on.
            config (dict): The game configuration dictionary.
            load_map_directly (bool): If True, starts directly in the load map menu.
        """
        self.window = window
        self.config = config

        self.state = GameState.LOAD_MAP if load_map_directly else GameState.ALGORITHM_MENU
        self.maze_data = None

        self.algorithm_menu = AlgorithmMenu(self.window, self.config)
        self.load_map_menu = LoadMapMenu(self.window, self.config)
        self.game_logic = None

    def _start_gameplay(self, maze_data: dict):
        """
        Helper method to transition to gameplay state after a maze is selected/generated.
        """
        self.maze_data = maze_data
        self.game_logic = GameLogic(self.window, self.maze_data, self.config)
        self.state = GameState.GAMEPLAY

    def update(self, events: list[pygame.event.Event]) -> str | None:
        """
        Updates the logic for the current game state based on a list of events.

        Args:
            events (list[pygame.event.Event]): A list of all Pygame events for the current frame.

        Returns:
            str | None: An action string (e.g., "back", "pause") to be handled by the Engine,
                        or None if no state transition is required.
        """
        if self.state == GameState.ALGORITHM_MENU:
            action = self.algorithm_menu.update(events) # Pass all events
            if action == "predefined":
                predefined_maze_generator = Predefined(self.config)
                self._start_gameplay(predefined_maze_generator.get_maze())
            elif action == "back":
                return "back"
            
        elif self.state == GameState.LOAD_MAP:
            action = self.load_map_menu.update(events) # Pass all events
            if action == "map_1":
                predefined_maze_generator = Predefined(self.config)
                self._start_gameplay(predefined_maze_generator.get_maze())
            elif action == "back":
                return "back"
            
        elif self.state == GameState.GAMEPLAY:
            # GameLogic handles its own internal events and updates, and pygame.key.get_pressed()
            game_action = self.game_logic.update(events) # Pass all events
            if game_action == "pause":
                return "pause"

        return None

    def draw(self):
        """
        Renders the visuals for the current game state.
        """
        if self.state == GameState.ALGORITHM_MENU:
            self.algorithm_menu.draw()
        elif self.state == GameState.LOAD_MAP:
            self.load_map_menu.draw()
        elif self.state == GameState.GAMEPLAY:
            self.game_logic.draw()