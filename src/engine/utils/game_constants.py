# src/engine/utils/game_constants.py

class GameConstants:
    """
    A class to hold engine-wide constants and default settings that are not
    intended to be easily modified by the end-user via settings.json.
    These values represent core design choices for the engine's behavior and UI.
    """
    # UI Constants
    MENU_FONT_SIZE: int = 48
    MENU_COOLDOWN_MS: int = 200
    SPLASH_DURATION_MS: int = 2500 # milliseconds