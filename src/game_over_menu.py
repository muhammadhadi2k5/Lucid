import pygame

from .menu import Button


class GameOverMenu:
    """Game-over screen: "GAME OVER" title + Restart/Main Menu buttons."""

    TITLE_COLOR = (220, 30, 30)  # red, matches the car's hit-flash and low-health color

    BUTTON_BASE_COLOR = (255, 90, 40)
    BUTTON_HOVER_COLOR = (74, 26, 130)
    BUTTON_PRESSED_COLOR = (46, 16, 82)

    BUTTON_BASE_TEXT_COLOR = (0, 0, 0)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont("consolas,couriernew,monospace", 60, bold=True)
        self.button_font = pygame.font.SysFont("consolas,couriernew,monospace", 28, bold=True)

        center_x = screen_width / 2
        self.restart_button = Button(
            center_x, screen_height * 0.55, 240, 60, "RESTART", self.button_font,
            self.BUTTON_BASE_COLOR, self.BUTTON_HOVER_COLOR, self.BUTTON_PRESSED_COLOR,
            self.BUTTON_BASE_TEXT_COLOR, self.BUTTON_HOVER_TEXT_COLOR,
        )
        self.exit_button = Button(
            center_x, screen_height * 0.68, 240, 60, "MAIN MENU", self.button_font,
            self.BUTTON_BASE_COLOR, self.BUTTON_HOVER_COLOR, self.BUTTON_PRESSED_COLOR,
            self.BUTTON_BASE_TEXT_COLOR, self.BUTTON_HOVER_TEXT_COLOR,
        )

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_button_down = pygame.mouse.get_pressed()[0]
        self.restart_button.update(mouse_pos, mouse_button_down)
        self.exit_button.update(mouse_pos, mouse_button_down)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.restart_button.is_clicked(event.pos):
                return "restart"
            if self.exit_button.is_clicked(event.pos):
                return "exit"
        return None

    def draw(self, screen):
        title_surface = self.title_font.render("GAME OVER", True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(self.screen_width / 2, self.screen_height * 0.3))
        screen.blit(title_surface, title_rect)

        self.restart_button.draw(screen)
        self.exit_button.draw(screen)
        
