import pygame
from pygame.sprite import Sprite
from random import choice

from spacebattle.bulletfactory import StrongBulletFactory, SideBulletFactory


class Reward(Sprite):

    image = None
    _y_speed = 2.5
    factories = [StrongBulletFactory, SideBulletFactory]
    _sound_make = None
    _sound_get = None

    @staticmethod
    def get_random_reward(settings, screen, x, y):
        return Reward(settings, screen, choice(Reward.factories)(),  x, y)

    def __init__(self, settings, screen, bullet_factory,  x, y):
        super().__init__()
        self.screen = screen
        self.game_settings = settings
        self.bullet_factory = bullet_factory
        self.image = self.bullet_factory.image
        self.rect = self.bullet_factory.rect
        self.x = float(x)
        self.y = float(y)
        if self._sound_make is None:
            self._sound_make = pygame.mixer.Sound('media/newreward.ogg')
        self._sound_make.play()
        if self._sound_get is None:
            self._sound_get = pygame.mixer.Sound('media/getreward.ogg')

    def update(self):
        """Обновление положения снаряд.
           Вызывается перед отрисовкой каждого кадра"""
        self.y += self._y_speed
        if self.has_removed():
            self.kill()

    def blit_me(self):
        """Рисует снаряд на экране self.screen"""
        self.rect.centerx = round(self.x)
        self.rect.bottom = round(self.y)
        self.screen.blit(self.image, self.rect)

    def has_removed(self):
        """Опеределяет, вышла ли пуля за пределы экрана"""
        return self.y > self.screen.get_height()

    def play_get_sound(self):
        self._sound_get.play()
