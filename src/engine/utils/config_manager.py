import json
import os
from src.engine.utils.engine_constants import EngineConstants

class ConfigManager:
    DEFAULT_CONFIG = {
        "resolution": EngineConstants.DEFAULT_RESOLUTION,
        "fullscreen": EngineConstants.DEFAULT_FULLSCREEN,
        "borderless": EngineConstants.DEFAULT_BORDERLESS,
        "fps_limit": EngineConstants.DEFAULT_FPS_LIMIT,
        "fov": EngineConstants.DEFAULT_FOV,
        "scale": EngineConstants.DEFAULT_RENDER_SCALE,
        "draw_distance": EngineConstants.DEFAULT_DRAW_DISTANCE
    }

    def __init__(self, config_path="assets/settings.json"):
        self.config_path = config_path
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
            print(f"[ERROR] Could not save config file: {e}")