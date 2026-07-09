import pygame


class Button:
    """A clickable button styled like an old mechanical keycap: it sits
    raised above a dark "well", and presses flush down into it on click.
    """

    POP_HEIGHT = 6  # pixels the cap sits above the well when idle

    def __init__(self, center_x, center_y, width, height, label, font,
                 base_color, hover_color, pressed_color,
                 base_text_color, hover_text_color):
        # rect is the button's fixed footprint - used for hit-testing and as
        # the well's (socket's) position. The cap is drawn shifted relative
        # to this, so rect itself never moves.
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (center_x, center_y)
        self.label = label
        self.font = font

        self.base_color = base_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        # hover and pressed share a text color since they're both the same
        # (non-orange) hue family - only the base/idle color is orange
        self.base_text_color = base_text_color
        self.hover_text_color = hover_text_color

        self.hovered = False
        self.pressed = False

    def update(self, mouse_pos, mouse_button_down):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.pressed = self.hovered and mouse_button_down

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        # the well: a fixed dark socket the cap sits in
        pygame.draw.rect(screen, (25, 25, 25), self.rect)

        # the cap: popped up when idle, flush with the well when pressed
        offset = 0 if self.pressed else -self.POP_HEIGHT
        cap_rect = self.rect.move(0, offset)

        if self.pressed:
            face_color = self.pressed_color
            text_color = self.hover_text_color
        elif self.hovered:
            face_color = self.hover_color
            text_color = self.hover_text_color
        else:
            face_color = self.base_color
            text_color = self.base_text_color
        pygame.draw.rect(screen, face_color, cap_rect)

        # bevel: a lighter edge on top/left, darker on bottom/right, to sell
        # the raised-plastic look. Skipped while pressed, since a pressed key
        # sits flat and shouldn't look raised.
        if not self.pressed:
            light_edge = self._shade(face_color, 50)
            dark_edge = self._shade(face_color, -50)
            pygame.draw.line(screen, light_edge, cap_rect.topleft, cap_rect.topright, 3)
            pygame.draw.line(screen, light_edge, cap_rect.topleft, cap_rect.bottomleft, 3)
            pygame.draw.line(screen, dark_edge, cap_rect.bottomleft, cap_rect.bottomright, 3)
            pygame.draw.line(screen, dark_edge, cap_rect.topright, cap_rect.bottomright, 3)

        text_surface = self.font.render(self.label, True, text_color)
        text_rect = text_surface.get_rect(center=cap_rect.center)
        screen.blit(text_surface, text_rect)

    @staticmethod
    def _shade(color, amount):
        # nudges each RGB channel by `amount`, clamped to the valid 0-255 range
        return tuple(max(0, min(255, channel + amount)) for channel in color)


class StartMenu:
    """The temporary start screen: blinking "LUCID." title + Play/Exit buttons.

    This is a stand-in - functional now, styling comes later. handle_event()
    returns an action string ("play" / "exit" / None) when the player picks
    something, so Game can react without this class knowing anything about
    the rest of the game.
    """

    TITLE_COLOR = (255, 90, 40)      # same orange used for the car/road accents

    BUTTON_BASE_COLOR = (255, 90, 40)
    BUTTON_HOVER_COLOR = (74, 26, 130)    # dark retro purple - reads as "interactive"
    BUTTON_PRESSED_COLOR = (46, 16, 82)   # darker still - reads as "pushed in"

    BUTTON_BASE_TEXT_COLOR = (0, 0, 0)        # black reads fine on the orange
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)  # black isn't readable on the purple, so white

    CURSOR_BLINK_INTERVAL = 0.5  # seconds the cursor dot stays on, or off

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # A comma-separated font list lets pygame pick whichever monospace
        # "coding" font is actually installed on this machine.
        self.title_font = pygame.font.SysFont("consolas,couriernew,monospace", 72, bold=True)
        self.button_font = pygame.font.SysFont("consolas,couriernew,monospace", 32, bold=True)

        self.cursor_visible = True
        self.cursor_timer = 0.0

        center_x = screen_width / 2
        self.play_button = Button(
            center_x, screen_height * 0.55, 220, 60, "PLAY", self.button_font,
            self.BUTTON_BASE_COLOR, self.BUTTON_HOVER_COLOR, self.BUTTON_PRESSED_COLOR,
            self.BUTTON_BASE_TEXT_COLOR, self.BUTTON_HOVER_TEXT_COLOR,
        )
        self.exit_button = Button(
            center_x, screen_height * 0.68, 220, 60, "EXIT", self.button_font,
            self.BUTTON_BASE_COLOR, self.BUTTON_HOVER_COLOR, self.BUTTON_PRESSED_COLOR,
            self.BUTTON_BASE_TEXT_COLOR, self.BUTTON_HOVER_TEXT_COLOR,
        )

    def update(self, dt):
        # flips cursor_visible on/off every CURSOR_BLINK_INTERVAL seconds
        self.cursor_timer += dt
        if self.cursor_timer >= self.CURSOR_BLINK_INTERVAL:
            self.cursor_timer = 0.0
            self.cursor_visible = not self.cursor_visible

        mouse_pos = pygame.mouse.get_pos()
        mouse_button_down = pygame.mouse.get_pressed()[0]
        self.play_button.update(mouse_pos, mouse_button_down)
        self.exit_button.update(mouse_pos, mouse_button_down)

    def handle_event(self, event):
        # fire on release (not press) so the "pressed" visual actually gets
        # a chance to show up on screen before the action happens
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.play_button.is_clicked(event.pos):
                return "play"
            if self.exit_button.is_clicked(event.pos):
                return "exit"
        return None

    def draw(self, screen):
        # Render "LUCID" at a fixed position first, then draw the cursor dot
        # right after it - keeping the dot separate stops the title jittering
        # sideways every time the cursor blinks on/off.
        title_surface = self.title_font.render("LUCID", True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(self.screen_width / 2, self.screen_height * 0.3))
        screen.blit(title_surface, title_rect)

        if self.cursor_visible:
            cursor_surface = self.title_font.render(".", True, self.TITLE_COLOR)
            screen.blit(cursor_surface, (title_rect.right + 6, title_rect.top))

        self.play_button.draw(screen)
        self.exit_button.draw(screen)
