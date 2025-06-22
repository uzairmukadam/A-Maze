import pygame
from src.game.utils.config_manager import ConfigManager

from src.game.screens.splash_screen import SplashScreen
from src.game.screens.main_menu import MainMenu
from src.game.game import Game
from src.game.screens.pause_menu import PauseMenu


class GameState:
    """
    Defines the distinct states of the game engine.
    Used to control which screen or game component is currently active.
    """
    SPLASH = "splash"
    MAIN_MENU = "main_menu"
    GAME = "game"
    PAUSE_MENU = "pause_menu"

class Engine:
    """
    The main game engine responsible for managing the game loop, window,
    overall game states, and delegating updates/drawing to current screens/gameplay.
    """
    def __init__(self, title="PyWare"):
        """
        Initializes the Pygame engine, game configuration, window, and initial game states.

        Args:
            title (str): The title to display on the game window.
        """
        pygame.init()

        self.version = "1.0.0"

        self.config = ConfigManager().config

        self.title = title
        self.window = None
        self.create_window()

        self.clock = pygame.time.Clock()
        self.running = False
        self.state = GameState.SPLASH

        self.splash_screen = SplashScreen(self.window)
        self.main_menu = MainMenu(self.window)
        self.game = None
        self.pause_menu = PauseMenu(self.window)

        self._current_events = []

    def create_window(self):
        """
        Creates and configures the Pygame display window based on settings from ConfigManager.
        Handles resolution, fullscreen, and borderless modes.
        """
        width, height = self.config["resolution"]
        flags = pygame.RESIZABLE

        if self.config.get("fullscreen", False):
            flags |= pygame.FULLSCREEN
        if self.config.get("borderless", False):
            flags |= pygame.NOFRAME
        
        self.window = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(self.title)

    def event_handler(self):
        """
        Processes Pygame events, clears the event list, and adds new events.
        Handles the pygame.QUIT event to stop the game.
        """
        self._current_events.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self._current_events.append(event)

    def update(self):
        """
        Updates the current game state and delegates update logic to the active screen or game.
        Handles state transitions based on actions returned by updated components.
        """
        if self.state == GameState.SPLASH:
            if not self.splash_screen.update():
                self.state = GameState.MAIN_MENU

        elif self.state == GameState.MAIN_MENU:
            action = self.main_menu.update(self._current_events)
            if action == "start_game":
                self.game = Game(self.window, self.config)
                self.state = GameState.GAME
            elif action == "quit_game":
                self.running = False

        elif self.state == GameState.GAME:
            if self.game:
                action = self.game.update(self._current_events)
                if action == "main_menu":
                    self.state = GameState.MAIN_MENU
                    self.main_menu.reset_cooldown()
                    self.game = None
                elif action == "pause":
                    self.state = GameState.PAUSE_MENU

        elif self.state == GameState.PAUSE_MENU:
            action = self.pause_menu.update(self._current_events)
            if action == "resume":
                self.state = GameState.GAME
            elif action == "main_menu":
                self.state = GameState.MAIN_MENU
                self.main_menu.reset_cooldown()
                self.game = None

    def draw(self):
        """
        Clears the window and draws the elements of the current game state.
        """
        self.window.fill((0, 0, 0))

        if self.state == GameState.SPLASH:
            self.splash_screen.draw()

        elif self.state == GameState.MAIN_MENU:
            self.main_menu.draw()

        elif self.state == GameState.GAME:
            if self.game:
                self.game.draw()

        elif self.state == GameState.PAUSE_MENU:
            self.pause_menu.draw()

        pygame.display.flip()

    def run(self):
        """
        Starts the main game loop.
        Processes events, updates game logic, draws to the screen, and controls the framerate.
        """
        self.running = True
        while self.running:
            self.event_handler()
            self.update()
            self.draw()
            
            self.clock.tick(self.config["fps_limit"]) 

        pygame.quit()
