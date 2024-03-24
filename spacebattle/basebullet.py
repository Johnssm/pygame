import pygame
from pygame import draw
from pygame.sprite import Sprite


class BaseBullet(Sprite):

    _y_speed = 3.5
    _x_speed = 0
    _height = 20
    _image = pygame.Surface((7, _height))
    _rect = _image.get_rect()
    draw.line(_image, (250, 240, 200), (3, 0), (3, _height), 7)
    draw.line(_image, (250, 160, 120), (3, 0), (3, _height), 5)
    draw.line(_image, (250, 80, 20), (3, 0), (3, _height), 3)
    _sound = None  # звук выстрела

    def __init__(self, settings, screen, x, y):
        """Конструктор класса"""
        super().__init__()
        self.screen = screen
        self.game_settings = settings
        self.to_remove = False  # Удалять ли снаряд так как
        # он столкнулся с кораблем
        self.image = self._image
        self.rect = self._rect
        self.x = float(x)
        self.y = float(y)
        self.x_speed = self._x_speed
        self.y_speed = self._y_speed
        if self._sound is None:
            self._sound = pygame.mixer.Sound('media/piu.ogg')
        self._sound.play()
        self.strong = 5
        self.unremovable = False

    def update(self):
        """Обновление положения снаряд.
           Вызывается перед отрисовкой каждого кадра"""
        self.y -= self.y_speed
        self.x += self.x_speed

    def blit_me(self):
        """Рисует снаряд на экране self.screen"""
        self.rect.centerx = round(self.x)
        self.rect.top = round(self.y)
        self.screen.blit(self.image, self.rect)

    def has_removed(self):
        """Опеределяет, вышла ли пуля за пределы экрана"""
        return self.y < -self.rect.height or self.to_remove
