import pygame
import src.engine.utils.config_manager as config_manager
from src.engine.splash_screen import SplashScreen
from src.engine.input_handler import InputHandler
from src.engine.menu_screen import MenuScreen
from src.engine.settings_menu import SettingsMenu

class GameState:
    SPLASH = "splash"
    MENU = "menu"
    SETTINGS = "settings"
    GAME = "game"

class GameEngine:
    def __init__(self, title):
        pygame.init()

        self.config_manager = config_manager.ConfigManager()
        self.config = self.config_manager.config
        self.title = title 

        self.screen = None
        self._set_display_mode()

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = GameState.SPLASH
        self.input_value = None

        self.splash_screen = SplashScreen(self.screen)
        self.input_handler = InputHandler()
        self.menu_screen = MenuScreen(self.screen)
        self.settings_screen = SettingsMenu(self.screen, self.config_manager) 

    def _set_display_mode(self):
        """Sets the Pygame display mode based on current config settings and updates screen references.
           This method is *only* called on initial game start or resolution changes,
           NOT for window mode changes (which require restart)."""
        self.width, self.height = self.config["resolution"]
        flags = pygame.RESIZABLE
        if self.config["borderless"]:
            flags |= pygame.NOFRAME
        if self.config["fullscreen"]:
            flags |= pygame.FULLSCREEN
        
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption(self.title)

        self.width, self.height = self.screen.get_size()
        
        screens_to_update = [
            getattr(self, 'splash_screen', None),
            getattr(self, 'menu_screen', None),
            getattr(self, 'settings_screen', None)
        ]
        for screen_obj in screens_to_update:
            if screen_obj: 
                screen_obj.screen = self.screen


    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                if not self.config["fullscreen"] and not self.config["borderless"]:
                    self.config_manager.update_setting("resolution", [event.w, event.h])
                    self._set_display_mode()
            self.input_value = self.input_handler.handle_event(event)

    def update(self):
        previous_state = self.state 

        if self.state == GameState.SPLASH:
            if not self.splash_screen.update():
                self.state = GameState.MENU
        elif self.state == GameState.MENU:
            action = self.menu_screen.update(self.input_value)
            if action == "settings":
                self.state = GameState.SETTINGS
            if action == "exit":
                self.running = False
        elif self.state == GameState.SETTINGS:
            action = self.settings_screen.update(self.input_value)
            
            if action == "back":
                self.state = GameState.MENU
            elif action == "update_resolution":
                new_resolution = self.settings_screen.get_current_resolution()
                self.config_manager.update_setting("resolution", list(new_resolution))
                self._set_display_mode()
            elif action == "update_window_mode":
                mode = self.settings_screen.get_current_window_mode()
                self.config_manager.update_setting("fullscreen", mode == "Fullscreen")
                self.config_manager.update_setting("borderless", mode == "Borderless")
        
        if previous_state == GameState.SETTINGS and self.state == GameState.MENU:
            self.menu_screen.reset_cooldown()

        self.input_value = None


    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.state == GameState.SPLASH:
            self.splash_screen.draw()
        elif self.state == GameState.MENU:
            self.menu_screen.draw()
        elif self.state == GameState.SETTINGS:
            self.settings_screen.draw()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.event_handling()

            self.update()

            self.draw()

            self.clock.tick(self.config["fps_limit"])

        pygame.quit()