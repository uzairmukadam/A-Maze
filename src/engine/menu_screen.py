import pygame

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start Game", "Settings", "Load Map", "Exit"]
        self.selected_index = 0
        self.last_input_time = pygame.time.get_ticks()
        self.input_cooldown = 90

    def reset_cooldown(self):
        """Resets the input cooldown for this menu, typically called when re-entering the menu."""
        self.last_input_time = pygame.time.get_ticks()

    def update(self, input_value):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_input_time > self.input_cooldown:
            if input_value == "move_down":
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.last_input_time = current_time
            elif input_value == "move_up":
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.last_input_time = current_time
            
            if input_value == "select":
                self.last_input_time = current_time
                if self.selected_index == 0:
                    return "start"
                elif self.selected_index == 1:
                    return "settings"
                elif self.selected_index == 2:
                    return "load_map"
                elif self.selected_index == 3:
                    return "exit"
        
        return None

    def draw(self):
        font = pygame.font.Font(None, 48)

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_index else (150, 150, 150)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 200 + i * 50))
            self.screen.blit(text_surface, text_rect)