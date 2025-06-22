# src/game/utils/constants.py

class Constants:
    # Window and Display
    DEFAULT_RESOLUTION = [1280, 720]
    DEFAULT_FULLSCREEN = False
    DEFAULT_BORDERLESS = False
    DEFAULT_FPS_LIMIT = 60
    
    # Rendering
    FOV = 65
    MAX_RAY_DISTANCE = 20.0
    FADE_START_DISTANCE = 3.0
    CLIP_PLANE_DISTANCE = 0.1
    WALL_MAX_VIEWPORT_HEIGHT_RATIO = 0.7

    # Colors for 3D rendering
    WALL_COLOR = (80, 90, 100)    # Lighter blue-grey for main walls
    FLOOR_COLOR = (50, 60, 70)    # Lighter, but still distinct dark grey for the floor
    CEILING_COLOR = (100, 110, 120) # Noticeably lighter blue-grey for the ceiling
    END_WALL_COLOR = (50, 180, 255)     # Brighter Electric Blue for end block base
    END_WALL_GLOW_COLOR = (150, 220, 255) # Even brighter, lighter electric blue for glow effect

    # UI/Menu
    SPLASH_DURATION_MS = 2500
    MENU_FONT_SIZE = 48
    MENU_COOLDOWN_MS = 150
    
    # Player Constants
    PLAYER_SPEED = 0.04
    PLAYER_ROTATION_SPEED = 0.02
    PLAYER_COLLISION_RADIUS = 0.3
