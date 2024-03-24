import pygame

from spacebattle.basebullet import BaseBullet
from spacebattle.sidebullet import SideBullet
from spacebattle.strongbullet import StrongBullet


class BulletFactory:

    image = None
    rect = None

    def make_bullet(self, scene, game_settings, screen, x, y):
        pass


class BaseBulletFactory(BulletFactory):

    def make_bullet(self, scene, game_settings, screen, x, y):
        scene.add_bullet(BaseBullet(game_settings, screen, round(x), round(y)))


class StrongBulletFactory(BulletFactory):

    image = pygame.image.load('media/strongbulletreward.bmp')
    image.set_colorkey((0, 0, 0))
    rect = image.get_rect()

    def make_bullet(self, scene, game_settings, screen, x, y):
        scene.add_bullet(StrongBullet(game_settings, screen, round(x),
                                      round(y)))


class SideBulletFactory(BulletFactory):

    image = pygame.image.load('media/sidebulletreward.bmp')
    image.set_colorkey((0, 0, 0))
    rect = image.get_rect()

    def make_bullet(self, scene, game_settings, screen, x, y):
        scene.add_bullet(SideBullet(game_settings, screen, round(x),
                                    round(y), 0))
        scene.add_bullet(SideBullet(game_settings, screen, round(x),
                                    round(y), 30))
        scene.add_bullet(SideBullet(game_settings, screen, round(x),
                                    round(y), -30))
