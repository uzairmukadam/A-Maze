import json
import os
from src.game.constants import Constants

class ConfigManager:
    DEFAULT_CONFIG = {
        "resolution": Constants.DEFAULT_RESOLUTION,
        "fullscreen": Constants.DEFAULT_FULLSCREEN,
        "borderless": Constants.DEFAULT_BORDERLESS,
        "fps_limit": Constants.DEFAULT_FPS_LIMIT
    }

    def __init__(self, config_filename="settings.json"):
        """
        Initializes the ConfigManager.
        The config_filename is expected to be relative to the project root.
        """
        script_dir = os.path.dirname(__file__)
        game_dir = os.path.dirname(script_dir)
        src_dir = os.path.dirname(game_dir)
        project_root = os.path.dirname(src_dir)

        self.config_path = os.path.join(project_root, config_filename)
        self.config = self.load_config()

    def load_config(self):
        loaded_config = {}
        if not os.path.exists(self.config_path):
            print(f"[INFO] Config file '{self.config_path}' missing, creating default settings...")
            self.save_config(self.DEFAULT_CONFIG)
            loaded_config = self.DEFAULT_CONFIG
        else:
            try:
                with open(self.config_path, "r") as f:
                    loaded_config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Could not decode config file: {e}. Using default settings and overwriting.")
                loaded_config = self.DEFAULT_CONFIG
                self.save_config(self.DEFAULT_CONFIG)
            except IOError as e:
                print(f"[ERROR] Could not read config file '{self.config_path}': {e}. Using default settings.")
                loaded_config = self.DEFAULT_CONFIG

        current_config = self.DEFAULT_CONFIG.copy()
        for key in current_config:
            if key in loaded_config:
                current_config[key] = loaded_config[key]
        
        if current_config != loaded_config:
            print("[INFO] Config file updated with new default settings or missing keys, or removed old keys.")
            self.save_config(current_config)

        return current_config

    def save_config(self, config_data):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        try:
            with open(self.config_path, "w") as f:
                json.dump(config_data, f, indent=4)
        except IOError as e:
            print(f"[ERROR] Could not save config file '{self.config_path}': {e}")

