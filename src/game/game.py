import os
import json

from src.game.screens.map_menu import MapMenu
from src.game.game_logic.game_logic import GameLogic
from src.game.screens.game_over_menu import GameOverMenu

class GameState:
    MAP_MENU = "map_menu"
    GAMEPLAY = "gameplay"
    GAME_OVER = "game_over"

class Game:
    def __init__(self, window, config):
        self.window = window
        self.config = config

        self.maps = self.get_maps()
        self.current_map = None

        self.state = GameState.MAP_MENU

        self.map_menu = MapMenu(self.window, self.maps)
        self.game_logic = None
        self.game_over_screen = None

    def read_files(self, relative_dir="assets/maps"):
        """
        Reads JSON map files from a specified directory relative to the project root.
        This makes the map loading more robust regardless of the current working directory.
        """
        files = []

        current_file_dir = os.path.dirname(__file__)
        src_dir = os.path.dirname(current_file_dir)
        project_root = os.path.dirname(src_dir)

        absolute_maps_dir = os.path.join(project_root, relative_dir)

        if not os.path.isdir(absolute_maps_dir):
            print(f"Error: Map directory not found at '{absolute_maps_dir}'")
            return []
        
        for filename in os.listdir(absolute_maps_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(absolute_maps_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        files.append({"filename": filename, "data": data})
                except json.JSONDecodeError as e:
                    print(f"Error: Skipping '{filename}'. Not a valid JSON file. Details: {e}")
                except Exception as e:
                    print(f"Error: Could not read '{filename}'. Details: {e}")

        return files

    def load_game(self, id):
        """Loads a specific maze based on its ID."""
        found_map = None
        for map_item in self.maps:
            if map_item["id"] == id:
                found_map = map_item
                break

        if found_map:
            self.current_map = found_map
            self.game_logic = GameLogic(self.window, self.config, self.current_map["data"])
        else:
            print(f"[ERROR] Map with ID {id} not found.")


    def verify_maps(self, files):
        """Verifies the structure of loaded maze files."""
        mazes = []
        required_keys = ["mazeName", "mazeData", "startCoordinate", "endCoordinate"]
        
        current_id = 0

        for file_data in files:
            is_valid = True
            for key in required_keys:
                if key not in file_data["data"]:
                    print(f"[WARNING] Map file '{file_data['filename']}' is missing key: '{key}'. Skipping.")
                    is_valid = False
                    break

            if is_valid:
                file_data["id"] = current_id
                current_id += 1
                mazes.append(file_data)

        return mazes

    def get_maps(self):
        """Retrieves and verifies all available map files."""
        files = self.read_files()
        return self.verify_maps(files)

    def update(self, events):
        """Updates the current game state."""
        action = None

        if self.state == GameState.MAP_MENU:
            action = self.map_menu.update(events)
            if action == "main_menu":
                return action
            elif isinstance(action, int):
                self.load_game(action)
                self.state = GameState.GAMEPLAY
            
        elif self.state == GameState.GAMEPLAY:
            if self.game_logic:
                action = self.game_logic.update(events)
            
            if action == "pause":
                return "pause"
            elif action == "game_over":
                total_time = self.game_logic.get_score() if self.game_logic else 0
                score = {"filename": self.current_map["filename"] if self.current_map else "Unknown", "total_time": total_time}
                self.game_over_screen = GameOverMenu(self.window, score)
                self.state = GameState.GAME_OVER

        elif self.state == GameState.GAME_OVER:
            if self.game_over_screen:
                action = self.game_over_screen.update(events)
            if action == "main_menu":
                return action

        return None

    def draw(self):
        """Draws the current game state."""
        if self.state == GameState.MAP_MENU:
            self.map_menu.draw()
        elif self.state == GameState.GAMEPLAY:
            if self.game_logic:
                self.game_logic.draw()
        elif self.state == GameState.GAME_OVER:
            if self.game_over_screen:
                self.game_over_screen.draw()

