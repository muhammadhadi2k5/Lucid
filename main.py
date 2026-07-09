import pygame

# Window size, in pixels. Defined once here so every other class can
# reference these same numbers instead of guessing at hardcoded values.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


class Game:
    """Owns the main window and the game loop."""

    def __init__(self):
        # pygame.init() sets up all of pygame's internal systems
        # (display, input, timing, etc.) — must be called before anything else.
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lucid Gears")

        # Clock lets us cap the loop at a fixed frame rate (see run() below).
        self.clock = pygame.time.Clock()

        # Controls whether the loop below keeps running.
        self.running = True

    def run(self):
        """The main game loop: handle input, update, draw. Repeat."""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()

            # Pause just long enough to keep us at FPS frames per second.
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        # pygame queues up everything that happened since we last checked
        # (key presses, mouse clicks, the window's close button, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self):
        # Nothing to update yet — this is where car/obstacle movement
        # will go once those classes exist.
        pass

    def _draw(self):
        # Fill the whole screen with black before drawing anything else,
        # otherwise each frame would paint over the last one and smear.
        self.screen.fill((0, 0, 0))

        # Flip the newly drawn frame onto the actual visible window.
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
