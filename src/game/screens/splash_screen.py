# src/game/screens/splash_screen.py
import pygame
from src.game.constants import Constants

class SplashScreen:
    """
    Manages the display and transitions of the game's splash screen sequence.
    Displays a series of text messages with fade-in/fade-out effects.
    """
    def __init__(self, window):
        """
        Initializes the SplashScreen with the display window and predefined sequence.

        Args:
            window (pygame.Surface): The main display surface for rendering.
        """
        self.window = window

        self.sequence = [
            {"text": "Made by Uzair", "font_size_ratio": 0.05},
            {"text": "A-Maze", "font_size_ratio": 0.15}
        ]

        self.current_index = 0
        self.start_time = pygame.time.get_ticks()
        
        self.duration = Constants.SPLASH_DURATION_MS
        self.fade_in_time = 1000
        self.fade_out_duration = 500
        self.fade_out_start = self.duration - self.fade_out_duration

        self.alpha = 0

    def update(self):
        """
        Updates the state of the splash screen, including alpha values for fading
        and transitioning to the next item in the sequence.

        Returns:
            bool: True if the splash screen sequence is still ongoing, False if it has finished.
        """
        if self.current_index >= len(self.sequence):
            return False

        elapsed_time = pygame.time.get_ticks() - self.start_time

        if elapsed_time < self.fade_in_time:
            self.alpha = min(255, int((elapsed_time / self.fade_in_time) * 255))
        elif elapsed_time < self.fade_out_start:
            self.alpha = 255
        else:
            fade_out_elapsed = elapsed_time - self.fade_out_start
            self.alpha = max(0, int(255 - (fade_out_elapsed / self.fade_out_duration) * 255))

        if elapsed_time >= self.duration:
            self.current_index += 1
            self.start_time = pygame.time.get_ticks()
            self.alpha = 0

        return self.current_index < len(self.sequence)

    def draw(self):
        """
        Draws the current text item of the splash screen to the window with the calculated alpha.
        """
        if self.current_index >= len(self.sequence):
            return

        current_sequence_item = self.sequence[self.current_index]
        
        font_size = int(self.window.get_height() * current_sequence_item["font_size_ratio"])
        font = pygame.font.Font(None, font_size)

        text_surface = font.render(current_sequence_item["text"], True, (255, 255, 255))
        text_surface.set_alpha(self.alpha)

        text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window.blit(text_surface, text_rect)
