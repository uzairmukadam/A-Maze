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
    def __init__(self, title="UziWare"):
        pygame.init()
        self.engine_version = "v1.0.0"

        self.config = ConfigManager().config
        
        self.title = title
        self.window = None
        self.set_window()
        
        self.clock = pygame.time.Clock()
        self.running = None
        self.state = GameState.SPLASH

        self.splash_screen = SplashScreen(self.window)
        self.main_menu = MainMenu(self.window)
        self.pause_menu = PauseMenu(self.window)
        self.game = None

    def set_window(self):
        self.width, self.height = self.config["resolution"]
        flags = pygame.RESIZABLE
        if self.config["borderless"]:
            flags |= pygame.NOFRAME
        if self.config["fullscreen"]:
            flags |= pygame.FULLSCREEN
        
        self.window = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption(self.title)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.event = event

    def update(self):
        if self.state == GameState.SPLASH:
            if not self.splash_screen.update():
                self.state = GameState.MAIN_MENU

        elif self.state == GameState.MAIN_MENU:
            action = self.main_menu.update(self.event)
            if action == "start_game":
                self.game = Game(self.window)
                self.state = GameState.GAME
            elif action == "quit":
                self.running = False

        elif self.state == GameState.GAME:
            action = self.game.update(self.event)
            if action == "back":
                self.state = GameState.MAIN_MENU
                self.main_menu.reset_cooldown()
            elif action == "pause":
                self.state = GameState.PAUSE_MENU

        elif self.state == GameState.PAUSE_MENU:
            action = self.pause_menu.update(self.event)
            if action == "resume":
                self.state = GameState.GAME
            elif action == "exit":
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
            self.event_handler()  # Handles user events
            self.update()  # Updates game logic
            self.draw()  # Renders updated visuals
            
            self.clock.tick(self.config["fps_limit"])

        pygame.quit()
