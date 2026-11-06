import pygame
import pytmx
from .Physics import ObstacleRect


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx.width * self.tmx.tilewidth
        self.height = self.tmx.height * self.tmx.tileheight

        self.collidables = []
        self.spikes = []

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def render(self, surface):
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile_image in layer.tiles():
                    surface.blit(tile_image, (x * self.tmx.tilewidth,
                                              (y + 1) * self.tmx.tileheight - tile_image.get_rect().height))

    def load_obstacles(self):
        for obj in self.tmx.objects:
            if obj.name == 'spawn':
                self.spawn_point = (obj.x, obj.y)
            elif obj.name == 'goal':
                self.goal = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "spikes":
                self.spikes.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            else:
                self.collidables.append(ObstacleRect(obj.x, obj.y, obj.width, obj.height))

    def make_map(self):
        self.render(self.surface)
        self.load_obstacles()
        return self.surface.convert_alpha()
