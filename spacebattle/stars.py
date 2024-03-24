from pygame import draw
from random import randint, normalvariate, choice


class Stars:
    """Класс для представления звезд на заднем плане игры"""
    def __init__(self, settings, screen):
        """Конструктор класса"""
        self.screen = screen
        self.game_settings = settings
        self.screen_rect = self.screen.get_rect()
        self.stars_speed = 0.3
        self.star_heigh_2 = 6  # Половина высоты звезды

        # Размещаем звезды на экране
        self.stars = []
        for i in range(0, 60):
            self.stars.append(self.generate_star())

    def update(self):
        """Обновление положения звезд.
           Вызывается перед отрисовкой каждого кадра"""
        for star in self.stars:
            self.move_star(star)

    def blit_me(self):
        """Рисует звезды на экране self.screen"""
        for star in self.stars:
            self.draw_star(star['color'], star['x'], star['y'])

    def draw_star(self, color, x, y):
        """ Рисует звезду
            self - экземпляр класса stars
            color - кортеж из трех чисел от 0 до 255, задающих
                    красный, зеленый и сисний компоненты цвета
            x, y - координаты центра звезды"""

        draw.line(self.screen, color, (x + 2, y), (x + 5, y), 3)
        draw.line(self.screen, color, (x - 2, y), (x - 5, y), 3)
        draw.line(self.screen, color, (x, y + 2), (x, y + 5), 3)
        draw.line(self.screen, color, (x, y - 2), (x, y - 5), 3)

    def generate_star(self):
        """Создает словарь с описанием звезды"""
        x = randint(0, self.screen_rect.width)  # randint - random integer
        y = randint(0, self.screen_rect.height)
        star_speed = normalvariate(0.2, 0.07)
        if star_speed <= 0.03:
            star_speed = 0.03

        color_init = choice(((200, 0, 50), (230, 230, 100), (100, 200, 230), (200, 200, 200)))

        red = int(color_init[0] + normalvariate(0, 20))
        if red > 255:
            red = 255
        elif red < 0:
            red = 0

        green = int(color_init[1] + normalvariate(0, 20))
        if green > 255:
            green = 255
        elif green < 0:
            green = 0

        blue = int(color_init[2] + normalvariate(0, 20))
        if blue > 255:
            blue = 255
        elif blue < 0:
            blue = 0

        return {'x': x,  'y': y, 'y_float': y, 'speed': star_speed, 'color': (red, green, blue)}

    def move_star(self, star):
        """Эмулирует движение звезд на заднем плане"""
        y_float = star['y_float']
        y_float += star['speed']
        if y_float > self.screen_rect.height + self.star_heigh_2:
            y_float = -self.star_heigh_2
            star['x'] = randint(0, self.screen_rect.width)
        star['y'] = int(y_float)
        star['y_float'] = y_float
