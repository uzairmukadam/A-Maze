import pygame

from src.engine.utils.config_manager import ConfigManager
from src.engine.screens.splash_screen import SplashScreen
from src.engine.screens.main_menu import MainMenu
from src.engine.screens.pause_menu import PauseMenu
from src.game.game import Game

class GameState:
    SPLASH = "splash"
    MAIN_MENU = "main_menu"
    GAME = "game"
    PAUSE_MENU = "pause_menu"

class Engine:
    def __init__(self, title: str = "UziWare"):
        pygame.init()
        self.engine_version = "v1.0.0"

        self.config = ConfigManager().config
        
        self.title = title
        self.window = None
        self._set_window()
        
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = GameState.SPLASH

        self.splash_screen = SplashScreen(self.window)
        self.main_menu = MainMenu(self.window)
        self.pause_menu = PauseMenu(self.window)
        self.game = None

        self._current_events = []

    def _set_window(self):
        width, height = self.config["resolution"]
        flags = pygame.RESIZABLE
        if self.config.get("borderless", False):
            flags |= pygame.NOFRAME
        if self.config.get("fullscreen", False):
            flags |= pygame.FULLSCREEN
        
        self.window = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(self.title)

    def event_handler(self):
        self._current_events.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self._current_events.append(event)

    def update(self):
        if self.state == GameState.SPLASH:
            if not self.splash_screen.update(): 
                self.state = GameState.MAIN_MENU

        elif self.state == GameState.MAIN_MENU:
            action = self.main_menu.update(self._current_events)
            if action == "start_new_game":
                self.game = Game(self.window, self.config)
                self.state = GameState.GAME
            elif action == "load_map":
                self.game = Game(self.window, self.config)
                self.state = GameState.GAME
            elif action == "quit_game":
                self.running = False


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
            elif action == "main_menu":
                self.state = GameState.MAIN_MENU
                self.main_menu.reset_cooldown()

    def draw(self):
        self.window.fill((0, 0, 0))

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
        self.running = True
        while self.running:
            self.event_handler()
            self.update()
            self.draw()
            
            self.clock.tick(self.config["fps_limit"]) 

        pygame.quit()