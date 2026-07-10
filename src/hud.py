import math

import pygame


class HealthGauge:
    """Circular health display in the corner: a ring of segments (one per
    hit the car can take) wrapped around a placeholder speedometer face.
    The face is empty for now - a needle can go in once there's an actual
    speed mechanic to point at.
    """

    RADIUS = 45
    RING_WIDTH = 10
    GAP_DEGREES = 6

    FACE_COLOR = (20, 20, 30)
    FACE_EDGE_COLOR = (60, 60, 70)
    EMPTY_SEGMENT_COLOR = (55, 55, 62)
    FULL_COLOR = (255, 90, 40)
    LOW_COLOR = (220, 30, 30)

    def __init__(self, center_x, center_y):
        self.center = (center_x, center_y)

    def draw(self, screen, health, max_health, segments):
        pygame.draw.circle(screen, self.FACE_COLOR, self.center, self.RADIUS - self.RING_WIDTH)
        pygame.draw.circle(screen, self.FACE_EDGE_COLOR, self.center, self.RADIUS - self.RING_WIDTH, 2)

        rect = pygame.Rect(0, 0, self.RADIUS * 2, self.RADIUS * 2)
        rect.center = self.center

        fraction = health / max_health
        fill_color = self._blend(self.FULL_COLOR, self.LOW_COLOR, 1 - fraction)
        segment_health = max_health / segments

        gap = math.radians(self.GAP_DEGREES)
        segment_angle = (2 * math.pi / segments) - gap

        for i in range(segments):
            start = -math.pi / 2 + i * (2 * math.pi / segments) + gap / 2
            end = start + segment_angle
            filled = health > i * segment_health
            color = fill_color if filled else self.EMPTY_SEGMENT_COLOR
            pygame.draw.arc(screen, color, rect, start, end, self.RING_WIDTH)

    @staticmethod
    def _blend(color_a, color_b, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))
