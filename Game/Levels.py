import pygame
from .GameScene import GameScene
from .Player import Player
from .Map import Map
from .Camera import Camera
from . import settings
import os
from .UI import Font, Mouse


class Levels(GameScene):
    def __init__(self, goto_scene, level=0):
        self._goto_scene = goto_scene
        GameScene.__init__(self)

        self.levels = [
            'level_olia_test.tmx',
            "level_olia_test2.tmx",
            "level_olia_test_3.tmx",
            "level_olia_test4.tmx",
            "level_olia_test5.tmx",
        ]
        self.current_level = level

        self.level_complete = False
        self._fadeout_timer = 0
        self._fadeout_time = 2

        # sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.player = Player((0, 0), groups=(self.all_sprites,))
        self.camera = Camera()
        self._total_deaths = 0

        self.load_new_level(self.current_level)

    def load_new_level(self, level_num):
        self.all_sprites.empty()
        self.all_sprites.add(self.player)

        self.level_complete = False
        self._fadeout_timer = 0

        self.map = Map(os.path.join(settings.levels_folder, self.levels[level_num]))
        self.map_img = self.map.make_map()
        self.player.set_pos(self.map.spawn_point)
        self.camera.set_boundaries(self.map_img.get_rect())
        self.camera.set_pos(self.map.spawn_point)


    def render(self, surface):
        if Mouse.is_visible():
            Mouse.set_visible(False)

        if self.level_complete:
            surface.fill((220, 220, 220), special_flags=pygame.BLEND_MULT)
        else:
            surface.blit(self.map_img, (0, 0), area=self.camera.camera_rect)
            for sprite in self.all_sprites:
                sprite.render(surface, self.camera)

            if settings.DEBUG_DRAW:
                for obs in self.map.collidables:
                    obs.render(surface, self.camera)

    def respawn_player(self):
        self.player.health = self.player._max_health
        p_pos = self.player.rect.center
        s_pos = self.map.spawn_point
        c_pos = (s_pos[0]+(p_pos[0]-s_pos[0])//3, s_pos[1]+(p_pos[1]-s_pos[1])//3)
        self.player.set_pos(self.map.spawn_point)
        self.camera.set_pos(c_pos)
        self._total_deaths += 1

    def update(self, delta_time):
        self.camera.move_to(self.player.rect.center, delta_time)

        if not self.level_complete:
            # check if reached goal
            if self.map.goal.contains(self.player.rect):
                print("Level", self.current_level, "Complete!")
                self.level_complete = True
                self._fadeout_timer = self._fadeout_time

                # --- ДОДАНО ДЛЯ ЗБЕРЕЖЕННЯ ПРОГРЕСУ ---
                # Оновлюємо максимальний відкритий рівень, якщо пройшли новий
                if self.current_level == settings.MAX_UNLOCKED_LEVEL:
                    settings.MAX_UNLOCKED_LEVEL += 1
                    print(f"New level unlocked: {settings.MAX_UNLOCKED_LEVEL}")
                # --------------------------------------

            # normal game loop updates
            self.player.update(delta_time, self.map)
            if self.player.health <= 0:
                self.respawn_player()

        # goal reached, fadeout animation
        elif self._fadeout_timer > 0:
            self._fadeout_timer -= delta_time

        # fadeout animation complete, load new level
        else:
            if self.current_level == len(self.levels) - 1:
                print("Game completed!")
                self._goto_scene("end_menu", self._total_deaths)
            else:
                self.current_level = (self.current_level + 1)
                self.load_new_level(self.current_level)


    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                if self.camera.boundaries is None:
                    self.camera.set_boundaries(self.map_img.get_rect())
                else:
                    self.camera.set_boundaries(None)
            elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                self._goto_scene("pause_menu")


