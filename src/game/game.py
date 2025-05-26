from src.game.screens.algorithm_menu import AlgorithmMenu
from src.game.screens.load_map_menu import LoadMapMenu

from src.game.maze_generator.predefined import Predefined

from src.game.game_logic.game_logic import GameLogic


class GameState:
    ALGORITHM_MENU = "algorith_menu"
    LOAD_MAP = "load_map"
    GAMEPLAY = "gameplay"
    GAME_OVER = "game_over"


class Game:
    def __init__(self, window, load_map=False):
        self.window = window

        self.state = GameState.LOAD_MAP if load_map else GameState.ALGORITHM_MENU
        self.maze = None

        self.algorithm_menu = AlgorithmMenu(self.window)
        self.load_map_menu = LoadMapMenu(self.window)
        self.game_logic = None

    def update(self, event):
        if self.state == GameState.ALGORITHM_MENU:
            action = self.algorithm_menu.update(event)
            if action == "predefined":
                maze = Predefined().get_maze()
                self.game_logic = GameLogic(maze)
                self.state = GameState.GAMEPLAY
            elif action == "back":
                return "back"
            
        elif self.state == GameState.LOAD_MAP:
            action = self.load_map_menu.update(event)
            if action == "predefined":
                maze = Predefined().get_maze()
                self.game_logic = GameLogic(maze)
                self.state = GameState.GAMEPLAY
            elif action == "back":
                return "back"
            
        elif self.state == GameState.GAMEPLAY:
            action = self.game_logic.update()
            if action == "pause":
                return "pause"

    def draw(self):
        if self.state == GameState.ALGORITHM_MENU:
            self.algorithm_menu.draw()
        elif self.state == GameState.LOAD_MAP:
            self.load_map_menu.draw()
        elif self.state == GameState.GAMEPLAY:
            self.game_logic.draw(self.window)