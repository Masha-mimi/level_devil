import pygame
from .Collidable import Collidable
from .. import settings


class ObstacleRect(Collidable):
    def __init__(self, x, y, width, height):
        Collidable.__init__(self, x, y, width, height)

    def render(self, surface, camera):
        if settings.DEBUG_DRAW:
            pygame.draw.rect(surface, settings.DEBUG_DRAW_COLOR,
                             pygame.Rect(camera.get_relative_pos(self.rect.x, self.rect.y),
                                         (self.rect.width, self.rect.height)), 1)
