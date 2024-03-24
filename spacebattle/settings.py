class Settings():
    """Класс для хранения настроек"""

    def __init__(self):
        """Создание настроек игры"""
        self.screen_width = 1000
        self.screen_height = 600
        self.ship_x_speed = 3.5  # Горизонтальная скорость корабля игрока
        self.ship_y_speed = 2.8  # Вертикальная скорость корабля игрока
        self.frames_per_second = 60  # Кадров в секунду
        self.initial_lives = 5  # Количество жизней
        self.strong_ship_probability = 0.1
