import pygame

class SettingsMenu:
    def __init__(self, screen, config_manager):
        self.screen = screen
        self.config_manager = config_manager
        self.options = ["Resolution", "Window Mode", "Back"]
        self.selected_index = 0

        self.resolutions = [(1280, 720), (1920, 1080)]
        self.window_modes = ["Windowed", "Fullscreen", "Borderless"]
        
        self._set_initial_values()

        self.last_input_time = pygame.time.get_ticks()
        self.input_cooldown = 90
        
        self.restart_required = False

    def _set_initial_values(self):
        current_res = tuple(self.config_manager.config["resolution"])
        try:
            self.res_index = self.resolutions.index(current_res)
        except ValueError:
            self.res_index = 0

        is_fullscreen = self.config_manager.config["fullscreen"]
        is_borderless = self.config_manager.config["borderless"]

        if is_fullscreen:
            self.window_index = self.window_modes.index("Fullscreen")
        elif is_borderless:
            self.window_index = self.window_modes.index("Borderless")
        else:
            self.window_index = self.window_modes.index("Windowed")

    def update(self, input_value):
        current_time = pygame.time.get_ticks()
        action_to_return = None

        if current_time - self.last_input_time > self.input_cooldown:
            if input_value == "move_down":
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.last_input_time = current_time
            elif input_value == "move_up":
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.last_input_time = current_time
            elif input_value == "move_left":
                action_to_return = self._adjust_setting(-1)
                self.last_input_time = current_time
            elif input_value == "move_right":
                action_to_return = self._adjust_setting(1)
                self.last_input_time = current_time
            
            if input_value == "select":
                self.last_input_time = current_time 
                if self.selected_index == len(self.options) - 1:
                    action_to_return = "back"
                    self.restart_required = False
                elif self.selected_index == 0:
                    action_to_return = "update_resolution"
                elif self.selected_index == 1:
                    action_to_return = "update_window_mode"

        return action_to_return

    def _adjust_setting(self, direction):
        if self.selected_index == 0:
            self.res_index = (self.res_index + direction) % len(self.resolutions)
            return "update_resolution"
        elif self.selected_index == 1:
            self.window_index = (self.window_index + direction) % len(self.window_modes)
            self.restart_required = True
            return "update_window_mode"
        return None

    def get_current_resolution(self):
        return self.resolutions[self.res_index]

    def get_current_window_mode(self):
        return self.window_modes[self.window_index]

    def draw(self):
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 30)

        for i, option in enumerate(self.options):
            text = option
            if option == "Resolution":
                text += f": {self.resolutions[self.res_index][0]}x{self.resolutions[self.res_index][1]}"
            elif option == "Window Mode":
                text += f": {self.window_modes[self.window_index]}"

            color = (255, 255, 255) if i == self.selected_index else (150, 150, 150)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 200 + i * 50))
            self.screen.blit(text_surface, text_rect)

        if self.restart_required:
            restart_text_surface = small_font.render("Restart game for window mode changes to apply.", True, (255, 255, 0))
            restart_text_rect = restart_text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 70))
            self.screen.blit(restart_text_surface, restart_text_rect)