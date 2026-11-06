import pygame
import os
from .Physics import RigidBody
from .Animation import Animation, AnimatedSprite
from .UI import Font
from . import settings


class Player(RigidBody, pygame.sprite.Sprite):
    class State:
        idle = 0
        walking = 1
        running = 2
        jumping = 3
        falling = 4

    textures = None
    sounds = None

    @staticmethod
    def _load_resources():
        player_folder = os.path.join(settings.img_folder, 'Jungle Asset Pack', 'character_edited')
        if Player.textures is None:
            print("loading player textures")
            Player.textures = {
                'player-idle': pygame.image.load(os.path.join(player_folder, 'idle outline big.png')).convert_alpha(),
                'player-run': pygame.image.load(os.path.join(player_folder, 'run outline big.png')).convert_alpha(),
                'player-jump': pygame.image.load(os.path.join(player_folder, 'jump outline big.png')).convert_alpha(),
                'player-fall': pygame.image.load(os.path.join(player_folder, 'jump outline big.png')).convert_alpha(),
            }
        if Player.sounds is None:
            Player.sounds = {
                'jump': pygame.mixer.Sound(os.path.join(settings.music_folder, 'jump.wav')),
                'hurt': pygame.mixer.Sound(os.path.join(settings.music_folder, 'Sound_1.wav')),
            }
            Player.sounds['jump'].set_volume(0.25)
            Player.sounds['hurt'].set_volume(0.3)

    def __init__(self, spawn_point, groups, on_restart_level=None):
        self._load_resources()

        self.state = self.State.idle
        self.animation = Animation()
        self.animation.add(self.State.idle, Player.textures['player-idle'], 12, 8, 'right', offset=(-4, -3))
        self.animation.add(self.State.walking, Player.textures['player-run'], 8, 10, 'right', offset=(-4, -3))
        self.animation.add(self.State.jumping, Player.textures['player-jump'], 1, 1, 'right', offset=(-4, -3))
        self.animation.add(self.State.falling, Player.textures['player-fall'], 1, 1, 'right', offset=(-4, -3))

        self._layer = 2
        RigidBody.__init__(self, *spawn_point, 24, 50)

        self.pushable = False
        pygame.sprite.Sprite.__init__(self, groups)

        self.jump_speed = settings.PLAYER_JUMP_SPEED
        self.walk_speed = settings.PLAYER_WALK_SPEED
        self.can_jump = True
        self.facing = self.animation.sprites[self.state].default_facing

        self._max_health = 1
        self.health = self._max_health
        self._invincible_timer = 0
        self._invincible_time = 3

        # Колбек для функціоналу перезапуску рівня при отриманні шкоди
        self.on_restart_level = on_restart_level

    def set_pos(self, pos):
        self.rect.topleft = pos

    def _get_input(self):
        self.v_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.v_x += -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.v_x += 1

        if self.v_x < 0 and self.facing != 'left':
            self.facing = 'left'
        if self.v_x > 0 and self.facing != 'right':
            self.facing = 'right'

        self.v_x *= self.walk_speed

    def jump(self):
        if self.can_jump:
            Player.sounds['jump'].play()
            self.v_y = -self.jump_speed
            self.can_jump = False

    def do_physics(self, delta_time, map):
        colliding = RigidBody.do_physics(self, delta_time, map.collidables)
        if colliding['bottom']:
            self.can_jump = True

        return colliding

    def hurt(self, health_points=1):
        if self._invincible_timer == 0:
            self.health -= health_points
            Player.sounds["hurt"].play()
            self._invincible_timer = self._invincible_time

            # Якщо передано функцію перезапуску рівня — викликаємо її одразу при отриманні шкоди
            if self.on_restart_level:
                self.on_restart_level()

    def _change_states(self):
        if self.v_y < 0:
            self.state = self.State.jumping
        elif self.v_y > 100:
            self.state = self.State.falling
            self.can_jump = False
        else:
            if abs(self.v_x) > 0 and self.state != self.State.walking:
                self.state = self.State.walking
            elif abs(self.v_x) == 0 and self.state != self.State.idle:
                self.state = self.State.idle


    def _spikes_collision(self, spikes_list):
        for spikes in spikes_list:
            if self.rect.colliderect(spikes):
                self.hurt()

    def update(self, delta_time, map):
        if self._invincible_timer > 0:
            self._invincible_timer -= delta_time
            if self._invincible_timer < 0:
                self._invincible_timer = 0
        self._spikes_collision(map.spikes)

        self._get_input()
        self.do_physics(delta_time, map)
        self._change_states()
        self.animation.play(self.state, delta_time)

    def render(self, surface, camera):
        self.animation.render(surface, camera.get_relative_rect(self.rect), self.facing, self._invincible_timer)

        RigidBody.render(self, surface, camera)

        if settings.DEBUG_DRAW:
            Font.put_text(surface, ['idle', 'walk', 'run', 'jump', 'fall'][self.state],
                          camera.get_relative_pos(self.rect.left, self.rect.top - 32), (0, 255, 255))
