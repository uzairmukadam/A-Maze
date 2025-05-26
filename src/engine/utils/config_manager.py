import json
import os

class ConfigManager:
    DEFAULT_CONFIG = {
        "resolution": [1280, 720],
        "fullscreen": False,
        "borderless": False,
        "fps_limit": 60,
        "fov": 75,
        "scale": 1.0
    }

    def __init__(self, config_path="assets/settings.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """
        Loads the config file. If missing, creates a default.
        Merges loaded config with default settings to handle new config fields.
        """
        loaded_config = {}
        if not os.path.exists(self.config_path):
            print("[INFO] Config file missing, creating default settings...")
            self.save_config(self.DEFAULT_CONFIG)
            loaded_config = self.DEFAULT_CONFIG
        else:
            try:
                with open(self.config_path, "r") as f:
                    loaded_config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Could not decode config file: {e}. Using default settings.")
                loaded_config = self.DEFAULT_CONFIG
                self.save_config(self.DEFAULT_CONFIG)

        merged_config = self.DEFAULT_CONFIG.copy()
        merged_config.update(loaded_config)

        return merged_config

    def save_config(self, config_data):
        """Saves the given config data back to the file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config_data, f, indent=4)