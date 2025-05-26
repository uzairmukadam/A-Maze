# src/game/game_constants.py

class GameConstants:
    """
    A class to hold game-specific constants and default settings that are not
    intended to be easily modified by the end-user via settings.json.
    These values represent core design choices for gameplay mechanics.
    """
    # Player Constants
    PLAYER_SPEED: float = 0.05
    PLAYER_ROTATION_SPEED: float = 0.05
    PLAYER_COLLISION_RADIUS: float = 0.2

    # Debugging
    DEBUG_DRAW_MINIMAP: bool = True

    # Other game-specific constants can go here as needed