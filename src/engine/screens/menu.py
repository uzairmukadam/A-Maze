import pygame
from src.engine.utils.engine_constants import EngineConstants

class Menu:
    def __init__(self, window, options):
        self.window = window
        self.options = options
        self.selected_index = 0
        
        self.font = pygame.font.Font(None, EngineConstants.MENU_FONT_SIZE)
        self.cooldown_start_time = 0
        self.cooldown_duration = EngineConstants.MENU_COOLDOWN_MS

    def update(self, events):
        current_time = pygame.time.get_ticks()
        if current_time - self.cooldown_start_time < self.cooldown_duration:
            return None

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    self.reset_cooldown()
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    self.reset_cooldown()
                elif event.key == pygame.K_RETURN:
                    selected_event = self.options[self.selected_index].get("event")
                    if selected_event:
                        self.reset_cooldown()
                        return selected_event
        return None

    def draw(self):
        center_x = self.window.get_width() // 2
        start_y = self.window.get_height() // 2 - (len(self.options) * self.font.get_height()) // 2

        for i, option_data in enumerate(self.options):
            option_text = option_data["option"]
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = self.font.render(option_text, True, color)
            text_rect = text_surface.get_rect(center=(center_x, start_y + i * self.font.get_height()))
            self.window.blit(text_surface, text_rect)

    def reset_cooldown(self):
        self.cooldown_start_time = pygame.time.get_ticks()