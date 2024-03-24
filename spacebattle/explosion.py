import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    _images = []
    _visible = 60
    _phases = 5
    # Загружаем изображения с кадрами взрыва из файлов
    for i in range(_phases):
        _images.append(pygame.image.load(f'media/explosion{i}.bmp'))
        _images[i].set_colorkey((0, 0, 0))
    _rect = _images[0].get_rect()
    _sound = None

    def __init__(self, settings, screen, x, y):
        """Конструктор класса"""
        super().__init__()
        self.screen = screen
        self.game_settings = settings
        self.to_remove = False  # Нужно ли удалять корабль
        self.rect = Explosion._rect
        self.x = round(x)
        self.y = round(y)
        self.remains = Explosion._visible
        self.phase = 0
        if Explosion._sound is None:
            Explosion._sound = pygame.mixer.Sound('media/explosion.ogg')
        Explosion._sound.play(maxtime=Explosion._visible * 1000 //
                              self.game_settings.frames_per_second)

    def update(self):
        """Обновление фазу взрыва.
           Вызывается перед отрисовкой каждого кадра"""
        self.remains -= 1
        self.phase = (Explosion._visible - self.remains) // \
                     (Explosion._visible // Explosion._phases + 1)
        if self.remains <= 0:
            self.kill()

    def blit_me(self):
        """Рисует взрыв на экране self.screen"""
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.screen.blit(Explosion._images[self.phase], self.rect)
