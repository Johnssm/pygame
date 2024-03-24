import pygame

from spacebattle.simplealienship import SimpleAlienShip


class StrongAlienShip(SimpleAlienShip):
    _image = pygame.image.load('media/strongalien.bmp')
    _image.set_colorkey((255, 255, 255))
    _rect = _image.get_rect()
    _max_vitality = 20
    _y_speed = 1.5  # Вертикальная скорость вражеского корабля
    reward_probability = 0.3
