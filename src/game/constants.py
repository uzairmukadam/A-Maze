class Constants:
    # Window and Display
    DEFAULT_RESOLUTION = [1280, 720]
    DEFAULT_FULLSCREEN = False
    DEFAULT_BORDERLESS = False
    DEFAULT_FPS_LIMIT = 60
    
    # Rendering (Updated for 3D View)
    DEFAULT_FOV = 65
    DEFAULT_DRAW_DISTANCE = 10
    
    MAX_RAY_DISTANCE = 20.0
    FADE_START_DISTANCE = 3.0
    CLIP_PLANE_DISTANCE = 0.1

    WALL_MAX_VIEWPORT_HEIGHT_RATIO = 0.7

    # Colors for 3D rendering (RGB tuples)
    WALL_COLOR = (100, 110, 120)  # Desaturated Blue-Grey Stone
    FLOOR_COLOR = (45, 40, 35)    # Dark Earthy Brown-Grey
    CEILING_COLOR = (80, 90, 100) # Lighter Blue-Grey, subtle
    
    # Colors for highlighted walls around start/end blocks
    START_WALL_COLOR = (0, 150, 0) # Muted Green for walls around the start block (not currently used for wall color)
    END_WALL_COLOR = (120, 0, 120) # Deep Mystical Purple for end block base
    END_WALL_GLOW_COLOR = (200, 50, 200) # Brighter Purple for glow effect

    # UI/Menu
    SPLASH_DURATION_MS = 2500
    MENU_FONT_SIZE = 48
    MENU_COOLDOWN_MS = 150
    
    # Player Constants
    PLAYER_SPEED = 0.05
    PLAYER_ROTATION_SPEED = 0.03
    PLAYER_COLLISION_RADIUS = 0.2

    # Debugging
    DEBUG_DRAW_MINIMAP = True
