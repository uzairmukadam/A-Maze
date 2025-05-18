import json
import os

class ConfigManager:
    DEFAULT_CONFIG = {
        "resolution": [1280, 720],
        "fullscreen": False,
        "borderless": False,
        "fps_limit": 60
    }

    def __init__(self, config_path="assets/settings.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """Loads the config file, creating default settings if missing."""
        if not os.path.exists(self.config_path):
            print("[INFO] Config file missing, creating default settings...")
            self.save_config(self.DEFAULT_CONFIG)
        
        with open(self.config_path, "r") as f:
            return json.load(f)

    def save_config(self, config_data):
        """Saves the given config data back to the file."""
        with open(self.config_path, "w") as f:
            json.dump(config_data, f, indent=4)
    
    def update_setting(self, key, value):
        """Updates a specific setting and saves changes."""
        if key in self.config:
            self.config[key] = value
            self.save_config(self.config)
        else:
            print(f"[WARNING] Invalid config key: {key}")
