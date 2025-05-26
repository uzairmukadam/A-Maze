# src/engine/engine.py
import pygame

from src.engine.utils.config_manager import ConfigManager
from src.engine.utils.game_constants import GameConstants # Import GameConstants
from src.engine.screens.splash_screen import SplashScreen
from src.engine.screens.main_menu import MainMenu
from src.engine.screens.pause_menu import PauseMenu
from src.game.game import Game

class GameState:
    """
    Defines the possible states of the game engine.
    """
    SPLASH = "splash"
    MAIN_MENU = "main_menu"
    GAME = "game"
    PAUSE_MENU = "pause_menu"

class Engine:
    """
    The core game engine responsible for managing game states,
    event handling, updates, and rendering.
    """
    def __init__(self, title: str = "UziWare"):
        """
        Initializes the Pygame engine, loads configurations, and sets up screens.

        Args:
            title (str): The title of the game window.
        """
        pygame.init()
        self.engine_version = "v1.0.0"

        self.config = ConfigManager().config # Config for user-modifiable settings
        # GameConstants are accessed directly (no self.game_constants instance)
        
        self.title = title
        self.window = None
        self._set_window()
        
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = GameState.SPLASH

        # Initialize all possible game screens/states, passing config where appropriate
        self.splash_screen = SplashScreen(self.window) # No config needed here anymore for splash duration
        self.main_menu = MainMenu(self.window) # No config needed here for menu options
        self.pause_menu = PauseMenu(self.window) # No config needed here for menu options
        self.game = None

        self._current_events: list[pygame.event.Event] = []

    def _set_window(self):
        """
        Configures and sets up the Pygame display window based on settings.
        """
        width, height = self.config["resolution"]
        flags = pygame.RESIZABLE
        if self.config.get("borderless", False):
            flags |= pygame.NOFRAME
        if self.config.get("fullscreen", False):
            flags |= pygame.FULLSCREEN
        
        self.window = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(self.title)

    def event_handler(self):
        """
        Processes Pygame events for the current frame.
        Populates _current_events list and handles QUIT event.
        """
        self._current_events.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self._current_events.append(event)

    def update(self):
        """
        Updates the logic of the currently active game state.
        Handles state transitions based on actions returned by state updates.
        Passes all collected events to the active state.
        """
        if self.state == GameState.SPLASH:
            if not self.splash_screen.update(): 
                self.state = GameState.MAIN_MENU

        elif self.state == GameState.MAIN_MENU:
            action = self.main_menu.update(self._current_events)
            if action == "start_game":
                # Only config (user-modifiable) is passed to Game
                self.game = Game(self.window, self.config) 
                self.state = GameState.GAME
            elif action == "quit":
                self.running = False
            elif action == "settings":
                # For future: implement a settings menu here
                print("Settings menu not implemented yet.")


        elif self.state == GameState.GAME:
            action = self.game.update(self._current_events) 
            if action == "back":
                self.state = GameState.MAIN_MENU
                self.main_menu.reset_cooldown()
            elif action == "pause":
                self.state = GameState.PAUSE_MENU

        elif self.state == GameState.PAUSE_MENU:
            action = self.pause_menu.update(self._current_events)
            if action == "resume":
                self.state = GameState.GAME
            elif action == "exit":
                self.state = GameState.MAIN_MENU
                self.main_menu.reset_cooldown()

    def draw(self):
        """
        Renders the visuals of the currently active game state.
        """
        self.window.fill((0, 0, 0)) # Clear with black background

        if self.state == GameState.SPLASH:
            self.splash_screen.draw()
        elif self.state == GameState.MAIN_MENU:
            self.main_menu.draw()
        elif self.state == GameState.GAME:
            self.game.draw()
        elif self.state == GameState.PAUSE_MENU:
            self.pause_menu.draw()

        pygame.display.flip()

    def run(self):
        """
        Starts the main game loop.
        """
        self.running = True
        while self.running:
            self.event_handler()
            self.update()
            self.draw()
            
            # Use fps_limit from config (user-modifiable)
            self.clock.tick(self.config["fps_limit"]) 

        pygame.quit()