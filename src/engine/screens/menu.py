# src/engine/screens/menu.py
import pygame
from src.engine.utils.game_constants import GameConstants # Import GameConstants

class Menu:
    """
    Base class for creating interactive menus in Pygame.
    Handles navigation with arrow keys and selection with Enter.
    """
    def __init__(self, window: pygame.Surface, options: list[dict]): # Removed config
        """
        Initializes the Menu.

        Args:
            window (pygame.Surface): The Pygame surface to draw the menu on.
            options (list[dict]): A list of dictionaries, where each dict
                                  represents a menu option, e.g.,
                                  {"option": "Display Text", "event": "action_string"}.
        """
        self.window = window
        self.options = options
        self.current_index = 0
        self.last_input_time = pygame.time.get_ticks()
        # Use constants from GameConstants
        self.input_cooldown = GameConstants.MENU_COOLDOWN_MS 
        self.font = pygame.font.Font(None, GameConstants.MENU_FONT_SIZE)

    def reset_cooldown(self):
        """
        Resets the input cooldown for menu, typically called when re-entering the menu
        to prevent accidental input processing from previous states.
        """
        self.last_input_time = pygame.time.get_ticks()

    def update(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles arrow key navigation and selection based on a list of events.

        Args:
            events (list[pygame.event.Event]): A list of all Pygame events for the current frame.

        Returns:
            str | None: The 'event' string associated with the selected option,
                        or None if no option was selected or input is on cooldown.
        """
        current_time = pygame.time.get_ticks()

        for event in events:
            if event.type == pygame.KEYDOWN and current_time - self.last_input_time > self.input_cooldown:
                self.last_input_time = current_time
                
                if event.key == pygame.K_UP:
                    self.current_index = (self.current_index - 1) % len(self.options)
                    
                elif event.key == pygame.K_DOWN:
                    self.current_index = (self.current_index + 1) % len(self.options)

                elif event.key == pygame.K_RETURN:
                    return self.options[self.current_index]["event"]
            
        return None

    def draw(self):
        """
        Renders menu items with selection highlighting.
        """
        total_height = len(self.options) * (self.font.get_height() + 10)
        start_y = (self.window.get_height() - total_height) // 2 

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.current_index else (150, 150, 150)
            text_surface = self.font.render(option["option"], True, color)
            
            text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, start_y + i * (self.font.get_height() + 10)))
            self.window.blit(text_surface, text_rect)