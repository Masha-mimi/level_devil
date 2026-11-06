import pygame
import os
from .Font import Font
from .Mouse import Mouse
from .. import settings


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

    def __init__(self, pos, size, callback, image_path=None, inactive_image_path=None, text=None, active=True):
        self._load_resources()
        self.rect = pygame.Rect(pos, size)
        self._callback = callback
        self._mouse_in_rect = False
        self._active = active  # Додаємо атрибут активності

        if image_path:
            img = pygame.transform.scale(pygame.image.load(image_path), size)
        elif text:
            img = Font.get_render(text)
        else:
            # Створюємо порожню поверхню, якщо немає ні зображення, ні тексту, щоб уникнути помилки
            img = pygame.Surface(size, pygame.SRCALPHA)

        self._original_surface = img  # Зберігаємо оригінальне зображення
        self._text_surface = img
        self._text_rect = self._text_surface.get_rect()
        self._text_x = self.rect.x + (self.rect.width - self._text_rect.width)//2
        self._text_y = self.rect.y + (self.rect.height - self._text_rect.height)//2

        # Створюємо неактивну версію зображення
        if inactive_image_path:
            self._inactive_surface = pygame.transform.scale(pygame.image.load(inactive_image_path), size)
        else:
            self._inactive_surface = self._original_surface.copy()
            # Створюємо сірий фільтр
            gray_filter = pygame.Surface(self._inactive_surface.get_size(), pygame.SRCALPHA)
            gray_filter.fill((100, 100, 100, 150)) # Сірий колір з прозорістю
            self._inactive_surface.blit(gray_filter, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self._update_surface() # Встановлюємо початковий стан

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self._update_surface()

    def _update_surface(self):
        # Оновлюємо поверхню, яку малюємо, залежно від активності
        if self._active:
            self._text_surface = self._original_surface
        else:
            self._text_surface = self._inactive_surface

    def render(self, surface):
        surface.blit(self._text_surface, (self._text_x, self._text_y))

    def handle_events(self, event):
        if not self._active: # Не обробляємо події, якщо кнопка неактивна
            self._mouse_in_rect = False
            return

        if self.rect.collidepoint(*Mouse.get_pos()):
            if self._mouse_in_rect is False:
                self.select_sound.play()
                self._mouse_in_rect = True

        else:
            self._mouse_in_rect = False
        if self._mouse_in_rect and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.click_sound.play()
            self._callback()