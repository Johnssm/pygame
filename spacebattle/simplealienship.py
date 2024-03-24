import pygame
from pygame import draw
from pygame.sprite import Sprite


class SimpleAlienShip(Sprite):

    _image = pygame.image.load('media/alien.bmp')
    _image.set_colorkey((255, 255, 255))
    _rect = _image.get_rect()
    _y_speed = 2.1  # Вертикальная скорость вражеского корабля
    _max_vitality = 10
    _vitality_margin = 7
    _vitality_line_width = 4
    _vitality_color = (0, 102, 46)
    _damage_color = (109, 18, 23)
    half_width = _rect.width // 2
    ship_scores = 100
    reward_probability = 0.1

    def __init__(self, settings, screen, scene, x, y, reward=None):
        """Конструктор класса"""
        super().__init__()
        self.screen = screen
        self.game_settings = settings
        self.to_remove = False  # Нужно ли удалять корабль
        self.image = self._image
        self.rect = self._rect
        self.x = x
        self.y = float(y)
        self.vitality = self._max_vitality
        self.scene = scene
        self.reward = reward

    def update(self):
        """Обновление положения вражеского корабля.
           Вызывается перед отрисовкой каждого кадра"""
        self.y += self._y_speed

    def blit_me(self):
        """Рисует вражеский корабль на экране self.screen"""
        self.rect.centerx = self.x
        self.rect.bottom = round(self.y)
        self.screen.blit(self.image, self.rect)
        # Отображаем полоску оставшегося здоровья
        if self.vitality < self._max_vitality:
            rib_len = round(self.rect.width * self.vitality / self._max_vitality)
            draw.line(self.screen, self._vitality_color,
                      (self.rect.left, self.rect.top - self._vitality_margin),
                      (self.rect.left + rib_len, self.rect.top - self._vitality_margin),
                      self._vitality_line_width)
            draw.line(self.screen, self._damage_color,
                      (self.rect.left + rib_len + 1, self.rect.top - self._vitality_margin),
                      (self.rect.right, self.rect.top - self._vitality_margin),
                      self._vitality_line_width)

    def has_removed(self):
        """Опеределяет, вышел ли вражеский корабль за пределы экрана"""
        return self.y > self.game_settings.screen_height or self.to_remove

    def collision(self, other):
        self.vitality -= other.strong
        if self.vitality <= 0 or other.unremovable:
            self.scene.remove_alien(self, other)
        elif not other.unremovable:
            self.scene.remove_alien(None, other)
