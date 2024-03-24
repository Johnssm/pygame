import pygame
from pygame import draw
from spacebattle.basebullet import BaseBullet


class StrongBullet(BaseBullet):

    _y_speed = 4.5
    _height = 30
    _image = pygame.Surface((9, _height))
    _rect = _image.get_rect()
    draw.line(_image, (152, 76, 131), (5, 0), (5, _height), 9)
    draw.line(_image, (255, 133, 125), (5, 0), (5, _height), 7)
    draw.line(_image, (255, 161, 94), (5, 0), (5, _height), 5)
    draw.line(_image, (252, 181, 141), (5, 0), (5, _height), 3)
    draw.line(_image, (253, 194, 216), (5, 0), (5, _height), 1)

    def __init__(self, settings, screen, x, y):
        """Конструктор класса"""
        super().__init__(settings, screen, x, y)
        self.unremovable = True
