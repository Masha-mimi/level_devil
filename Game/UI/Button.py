import pygame
import os
from .Font import Font
from .Mouse import Mouse
from .. import settings


class Button:
    select_sound = None
    click_sound = None

    @staticmethod
    def _load_resources():
        if Button.select_sound is None:
            Button.select_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'zipclick.wav'))
            Button.click_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'klick1.wav'))
            Button.click_sound.set_volume(0.5)

    def __init__(self, pos, size, img, callback):
        self._load_resources()
        self.rect = pygame.Rect(pos, size)
        self._callback = callback
        self._mouse_in_rect = False

        img = pygame.transform.scale(img, size)
        self._text_surface = img
        self._text_rect = self._text_surface.get_rect()
        self._text_x = self.rect.x + (self.rect.width - self._text_rect.width)//2
        self._text_y = self.rect.y + (self.rect.height - self._text_rect.height)//2

    def render(self, surface):
        surface.blit(self._text_surface, (self._text_x, self._text_y))

    def handle_events(self, event):
        # if self.rect.collidepoint(*pygame.mouse.get_pos()):
        if self.rect.collidepoint(*Mouse.get_pos()):
            if self._mouse_in_rect is False:
                self.select_sound.play()
                self._mouse_in_rect = True

        else:
            self._mouse_in_rect = False
        if self._mouse_in_rect and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.click_sound.play()
            self._callback()