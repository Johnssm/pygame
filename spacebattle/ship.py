import pygame
from pygame.sprite import Sprite
from spacebattle.bulletfactory import BaseBulletFactory


class Ship(Sprite):

    def __init__(self, settings, screen, scene):
        """Конструктор класса"""
        super().__init__()
        self.screen = screen
        self.game_settings = settings
        self.direction_x = 0  # Направление движения корабля по горизонтали: 0 - стоит на мест
        # 1 - движется влево, 2 - движется вправо
        self.direction_y = 0  # Направление движения корабля по вертикали: 0 - стоит на месте,
        # 1 - движется вверх, 2 - движется вниз
        self.image = pygame.image.load('media/ship.bmp')
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.ship_bottom = screen.get_rect().bottom - 10
        self.ship_x_center = float(screen.get_rect().centerx)
        self.scene = scene
        self.bullet_factory = BaseBulletFactory()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction_x = 1
            elif event.key == pygame.K_RIGHT:
                self.direction_x = 2
            elif event.key == pygame.K_UP:
                self.direction_y = 1
            elif event.key == pygame.K_DOWN:
                self.direction_y = 2
            elif event.key == pygame.K_SPACE:
                self.bullet_factory.make_bullet(self.scene, self.game_settings, self.screen,
                                                self.ship_x_center, self.ship_bottom - self.rect.height)

        # Обрабатывам отпускание кнопки
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.direction_x == 1:
                self.direction_x = 0
            elif event.key == pygame.K_RIGHT and self.direction_x == 2:
                self.direction_x = 0
            elif event.key == pygame.K_UP and self.direction_y == 1:
                self.direction_y = 0
            elif event.key == pygame.K_DOWN and self.direction_y == 2:
                self.direction_y = 0

    def update(self):
        """Обновление положения корабля.
           Вызывается перед отрисовкой каждого кадра"""
        # Вычисляем новое положение корабля
        if self.direction_x == 1:
            # Движемся влево
            self.ship_x_center -= self.game_settings.ship_x_speed
            if self.ship_x_center < 0:
                self.ship_x_center = 0.0
        elif self.direction_x == 2:
            # Движемся вправо
            self.ship_x_center += self.game_settings.ship_x_speed
            if self.ship_x_center > self.game_settings.screen_width:
                self.ship_x_center = self.game_settings.screen_width

        if self.direction_y == 1:
            # Движемся вверх
            self.ship_bottom -= self.game_settings.ship_y_speed
            if self.ship_bottom < self.rect.height:
                self.ship_bottom = 0.0 + self.rect.height
        elif self.direction_y == 2:
            # Движемся вниз
            self.ship_bottom += self.game_settings.ship_y_speed
            if self.ship_bottom > self.game_settings.screen_height:
                self.ship_bottom = self.game_settings.screen_height

    def blit_me(self):
        """Рисует корабль на экране self.screen"""
        self.rect.centerx = round(self.ship_x_center)
        self.rect.bottom = round(self.ship_bottom)
        self.screen.blit(self.image, self.rect)

    def blit_me_at(self, x, y, count):
        """Рисует корабль на экране self.screen
        с координатами x, y. Повторяет изображение count раз
        :rtype: None"""
        rect = self.rect.copy()
        for i in range(count):
            rect.left = x + i * (rect.width + 5)
            rect.top = y
            self.screen.blit(self.image, rect)

    def set_bullet_factory(self, bullet_factory):
        self.bullet_factory = bullet_factory
