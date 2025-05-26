# src/engine/utils/config_manager.py
import json
import os

class ConfigManager:
    """
    Manages loading, saving, and accessing game configuration settings.
    Ensures a default configuration exists if no file is found or if it's invalid.
    This manager now focuses *only* on user-modifiable settings stored in settings.json.
    """
    # Only settings that the user can change via settings.json
    DEFAULT_CONFIG = {
        "resolution": [1280, 720],
        "fullscreen": False,
        "borderless": False,
        "fps_limit": 60,
        "fov": 75,
        "scale": 1.0,
        "draw_distance": 3 # Renamed from render_distance
    }

    def __init__(self, config_path: str = "assets/settings.json"):
        """
        Initializes the ConfigManager and loads the configuration.

        Args:
            config_path (str): The path to the configuration JSON file.
        """
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> dict:
        """
        Loads the config file. If missing, creates a default.
        Merges loaded config with default settings to handle new config fields
        and ensure all necessary settings are present.

        Returns:
            dict: The loaded and merged configuration dictionary.
        """
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

        merged_config = self.DEFAULT_CONFIG.copy()
        # Merge only keys that are in DEFAULT_CONFIG (to handle older config files gracefully)
        # This ensures we only keep the keys we expect in settings.json
        for key in merged_config:
            if key in loaded_config:
                merged_config[key] = loaded_config[key]
        
        # Check if the loaded config had extra keys not in DEFAULT_CONFIG (which we'll ignore)
        # or if DEFAULT_CONFIG added new keys (which we'll save)
        if merged_config != loaded_config: # Compare only the relevant keys
            print("[INFO] Config file updated with new default settings or missing keys, or removed old keys.")
            self.save_config(merged_config)

        return merged_config

    def save_config(self, config_data: dict):
        """Saves the given config data back to the file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        try:
            with open(self.config_path, "w") as f:
                json.dump(config_data, f, indent=4)
        except IOError as e:
            print(f"[ERROR] Could not save config file: {e}")