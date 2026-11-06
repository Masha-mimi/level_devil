from .GameScene import GameScene
from . import settings
import pygame
import os
from .UI import Mouse, Button, Font, CheckBox
import random


class StartMenu(GameScene):
    bg = None

    @staticmethod
    def _load_resources():
        if StartMenu.bg is None:
            StartMenu.bg = pygame.transform.smoothscale(pygame.image.load(os.path.join(settings.img_folder, "HUD", "menu.png")), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def __init__(self, goto_scene):
        self._goto_scene = goto_scene
        GameScene.__init__(self)
        self._load_resources()

        Mouse.set_visible(True)

        # self._title = Font.get_render(settings.WIN_TITLE, size="huge")
        self._title = pygame.image.load(os.path.join(settings.img_folder, "title_text.png"))
        self._text_rect = self._title.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._text_rect.height // 2

        y = self._text_rect.bottom + 250
        w, h = 40, 40

        # --- ЗМІНЕНО ---
        # Кнопка для 1-го рівня
        self.start_bttn_l1 = Button((settings.SCREEN_WIDTH // 22, y - 110), (w, h),
                                    image_path="Resources/images/HUD/portal_1.png",
                                    callback=lambda: goto_scene("level_manager", 0),
                                    active=True)

        # Кнопка для 2-го рівня
        self.start_bttn_l2 = Button((settings.SCREEN_WIDTH // 22 + 85, y - 125), (w, h),
                                    image_path="Resources/images/HUD/portal_1.png",
                                    inactive_image_path="Resources/images/HUD/soon_portal1.png",
                                    callback=lambda: goto_scene("level_manager", 1),
                                    active=(settings.MAX_UNLOCKED_LEVEL >= 1))

        # Кнопка для 3-го рівня
        self.start_bttn_l3 = Button((settings.SCREEN_WIDTH // 22 + 190, y - 110), (w, h),
                                    image_path="Resources/images/HUD/portal_1.png",
                                    inactive_image_path="Resources/images/HUD/soon_portal1.png",
                                    callback=lambda: goto_scene("level_manager", 2),
                                    active=(settings.MAX_UNLOCKED_LEVEL >= 2))
        # ---------------
        self.start_bttn_l4 = Button((settings.SCREEN_WIDTH // 22 + 250, y - 70), (w, h),
                                    image_path="Resources/images/HUD/portal_1.png",
                                    inactive_image_path="Resources/images/HUD/soon_portal1.png",
                                    callback=lambda: goto_scene("level_manager", 2),
                                    active=(settings.MAX_UNLOCKED_LEVEL >= 2))

        self.start_bttn_l5 = Button((settings.SCREEN_WIDTH // 22 + 210, y - 10), (w, h),
                                    image_path="Resources/images/HUD/portal_1.png",
                                    inactive_image_path="Resources/images/HUD/soon_portal1.png",
                                    callback=lambda: goto_scene("level_manager", 2),
                                    active=(settings.MAX_UNLOCKED_LEVEL >= 2))

        self.settings_bttn = Button((settings.SCREEN_WIDTH//40, y+90), (w, h),
                                    callback=lambda: goto_scene("settings_menu"),
                                    image_path="Resources/images/HUD/setings.png")

        self.exit_bttn = Button((settings.SCREEN_WIDTH//2, y+150), (w, h),
                                callback=lambda: goto_scene("quit"),
                                image_path="Resources/images/HUD/portal_1.png")

    def render(self, surface):
        surface.blit(self.bg, (0, 0))
        # Малюємо всі 3 кнопки порталів
        self.start_bttn_l1.render(surface)
        self.start_bttn_l2.render(surface)
        self.start_bttn_l3.render(surface)
        self.start_bttn_l4.render(surface)
        self.start_bttn_l5.render(surface)
        self.settings_bttn.render(surface)
        # self.credits_bttn.render(surface)


    def update(self, delta_time):
        # Оновлюємо стан активності кнопок у update, щоб вони ставали активними
        # якщо settings.MAX_UNLOCKED_LEVEL зміниться
        self.start_bttn_l2.active = (settings.MAX_UNLOCKED_LEVEL >= 1)
        self.start_bttn_l3.active = (settings.MAX_UNLOCKED_LEVEL >= 2)

    def handle_events(self, event):
        # Обробляємо події для всіх 3 порталів
        self.start_bttn_l1.handle_events(event)
        self.start_bttn_l2.handle_events(event)
        self.start_bttn_l3.handle_events(event)
        self.settings_bttn.handle_events(event)
        # self.credits_bttn.handle_events(event)
        self.exit_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
            self._goto_scene("quit")


class PauseMenu(GameScene):
    def __init__(self, goto_scene):
        self._goto_scene = goto_scene
        GameScene.__init__(self)
        Mouse.set_visible(True)
        w, h = 200, 60

        self._text_surface = Font.get_render("Paused", size="big")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._text_rect.height // 2

        self.continue_bttn = Button(((settings.SCREEN_WIDTH-w)//2, self._text_rect.bottom + 50), (w, h),
                                    image_path="Resources/images/HUD/buttons/continue_button.png",
                                    callback=lambda: goto_scene("previous"))

        self.settings_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 125), (w, h),
                                    image_path="Resources/images/HUD/buttons/settings_button.png",
                                    callback=lambda: goto_scene("settings_menu"))

        self.start_menu_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 200), (w, h),
                                      image_path="Resources/images/HUD/buttons/start_menu_button.png",
                                      callback=lambda: goto_scene("start_menu"))

        self.exit_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 275), (w, h),
                                image_path="Resources/images/HUD/buttons/exit_button.png",
                                callback=lambda: goto_scene("quit"))

    def render(self, surface):
        surface.fill((35, 25, 40))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        self.continue_bttn.render(surface)
        self.settings_bttn.render(surface)
        self.start_menu_bttn.render(surface)
        self.exit_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self.continue_bttn.handle_events(event)
        self.settings_bttn.handle_events(event)
        self.start_menu_bttn.handle_events(event)
        self.exit_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
            self._goto_scene("previous")


class SettingsMenu(GameScene):
    def __init__(self, goto_scene, update_display_config):
        self._goto_scene = goto_scene
        self._update_display_config = update_display_config

        GameScene.__init__(self)
        Mouse.set_visible(True)
        w, h = 50, 50

        self._text_surface = Font.get_render("Settings", size="big")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._text_rect.height//2

        self._fullscreen_checkbox = CheckBox((50, self._text_rect.bottom+50), "Fullscreen")
        self._fullscreen_checkbox.selected = settings.FULLSCREEN
        self._scale_checkbox = CheckBox((50, self._text_rect.bottom + 100), "Scale to 1280x720")
        self._scale_checkbox.selected = (settings.FINAL_HEIGHT != settings.SCREEN_HEIGHT)
        self._fps_checkbox = CheckBox((50, self._text_rect.bottom + 150), "Show FPS")
        self._fps_checkbox.selected = settings.SHOW_FPS

        self.continue_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 50), (70, 70),
                                    image_path="Resources/images/HUD/buttons/ok.png",
                                    callback=self._on_done)

    def _on_done(self):
        settings.SHOW_FPS = self._fps_checkbox.selected
        h = 720 if self._scale_checkbox.selected else 480
        self._update_display_config(self._fullscreen_checkbox.selected, h)
        self._goto_scene("previous")

    def render(self, surface):
        surface.fill((35, 25, 40))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        self._fullscreen_checkbox.render(surface)
        self._scale_checkbox.render(surface)
        self._fps_checkbox.render(surface)
        self.continue_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self._fullscreen_checkbox.handle_events(event)
        self._scale_checkbox.handle_events(event)
        self._fps_checkbox.handle_events(event)
        self.continue_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._goto_scene("previous")


class EndMenu(GameScene):
    class Confetti:
        def __init__(self, color):
            self.color = color
            self.speed = random.randint(200, 500)
            self.size = random.randint(2, 6)
            self.pos = [random.randrange(5, settings.SCREEN_WIDTH-5), 0]
            self._t = 0
            self._dx = 0

        def render(self, surface):
            pygame.draw.rect(surface, self.color, (self.pos, (self.size, self.size)))

        def update(self, delta_time):
            self.pos[1] += self.speed * delta_time
            if self.pos[1] >= settings.SCREEN_HEIGHT:
                self.pos[1] = 0
                self.pos[0] = random.randrange(5, settings.SCREEN_WIDTH-5)

            self._t += delta_time
            if self._t > 0.5:
                self._t = 0
                self._dx = [-50, 50][random.randint(0, 1)]
            self.pos[0] += self._dx*delta_time

    def __init__(self, goto_scene, total_deaths):
        self._goto_scene = goto_scene
        GameScene.__init__(self)
        Mouse.set_visible(True)
        self.victory_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'victory.wav'))
        self.victory_sound.set_volume(0.5)
        self._colors = [(250, 20, 20), (20, 250, 20), (250, 20, 250),
                        (250, 250, 20), (20, 250, 250), ]
        self._color_i = 0
        self._elapsed_time = 0
        self._confettis = [self.Confetti(self._colors[random.randrange(0, len(self._colors))]) for i in range(30)]

        w, h = 200, 70

        self._heading_text_surface = Font.get_render("Congratulations!!", size="big")
        self._heading_text_rect = self._heading_text_surface.get_rect()
        self._heading_text_x = (settings.SCREEN_WIDTH - self._heading_text_rect.width) // 2
        self._heading_text_y = self._heading_text_rect.height // 2

        self._text_surface = Font.get_render("You have completed your journey!", size="normal")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._heading_text_y + self._heading_text_rect.height*2

        self._death_text_surface = Font.get_render("Total Deaths:  %d" % (total_deaths,))
        self._death_text_rect = self._death_text_surface.get_rect()
        self._death_text_x = (settings.SCREEN_WIDTH - self._death_text_rect.width) // 2
        self._death_text_y = self._text_y + self._text_rect.height * 3 // 2

        button_y = self._death_text_y + self._death_text_rect.height

        self.start_menu_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, button_y), (w, h),
                                    image_path="Resources/images/HUD/buttons/start_menu_button.png",
                                    callback=lambda: goto_scene("start_menu"))

        self.exit_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, button_y + 125), (w, h),
                                    image_path="Resources/images/HUD/buttons/exit_button.png",
                                    callback=lambda: goto_scene("quit"))
        self.victory_sound.play()

    def render(self, surface):
        surface.fill((35, 25, 40))
        # surface.blit(self._heading_text_surface, (self._heading_text_x, self._heading_text_y))
        surface.blit(Font.get_render("Congratulations!!", color=self._colors[self._color_i], size="big"), (self._heading_text_x, self._heading_text_y))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        surface.blit(self._death_text_surface, (self._death_text_x, self._death_text_y))
        self.start_menu_bttn.render(surface)
        self.exit_bttn.render(surface)

        for confetti in self._confettis:
            confetti.render(surface)

    def update(self, delta_time):
        self._elapsed_time += delta_time
        if self._elapsed_time >= 0.25:
            self._elapsed_time = 0
            self._color_i = (self._color_i + 1)%len(self._colors)

        for confetti in self._confettis:
            confetti.update(delta_time)

    def handle_events(self, event):
        self.start_menu_bttn.handle_events(event)
        self.exit_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
            self._goto_scene("start_menu")
