import pygame
from spacebattle.basebullet import BaseBullet
from math import cos, sin, radians


class SideBullet(BaseBullet):

    _base_speed = 3.5
    _image = pygame.image.load('media/sidebullet.bmp')
    _image.set_colorkey((0, 0, 0))
    _rect = _image.get_rect()

    def __init__(self, settings, screen, x, y, angle):
        """Конструктор класса"""
        super().__init__(settings, screen, x, y)
        self.strong = 5
        rad_angle = radians(angle)
        self.x_speed = self._base_speed * sin(rad_angle)
        self.y_speed = self._base_speed * cos(rad_angle)

    def has_removed(self):
        """Опеределяет, вышла ли пуля за пределы экрана"""
        half_width = self.rect.width / 2
        return (self.y < -self.rect.height or self.x + half_width < 0
                or self.x - half_width > self.screen.get_width() or self.to_remove)
