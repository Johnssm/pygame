import os
import sys
import pygame

from spacebattle.mainscene import MainScene
from spacebattle.settings import Settings


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('media', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def start_screen():
    intro_text = ["КОСМИЧЕСКОЕ СРАЖЕНИЕ", "",
                  "Правила игры",
                  "Для перемещения используйте",
                  "клавиши со стрелками", "",
                  "Для выстрела исползуйте ПРОБЕЛ", "",
                  "Подбирайте призовые шары для",
                  "смены типов снарядов"]
    text_left = 10
    text_width = 0
    text_top = 50
    text_height = 0
    padding = 5

    fon = pygame.transform.scale(load_image('splashscreen.jpg'),
                                 pygame.display.get_window_size())
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    cur_text_top = text_top
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 127, 39))
        intro_rect = string_rendered.get_rect()
        text_width = max(text_width, intro_rect.width)
        cur_text_top += 10
        intro_rect.top = cur_text_top
        cur_text_top += intro_rect.height
        intro_rect.x = text_left
        text_width = max(text_width, intro_rect.right)
        text_height = intro_rect.bottom - text_top

    surf = pygame.Surface((text_width + 2 * padding, text_height + 2 * padding))
    surf.fill((0, 0, 0))
    surf.set_alpha(150)
    screen.blit(surf, (text_left - padding, text_top - padding))

    cur_text_top = text_top
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 127, 39))
        intro_rect = string_rendered.get_rect()
        text_width = max(text_width, intro_rect.width)
        cur_text_top += 10
        intro_rect.top = cur_text_top
        cur_text_top += intro_rect.height
        intro_rect.x = text_left
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    # Параметры
    game_settings = Settings()

    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()

    size = (game_settings.screen_width, game_settings.screen_height)  # Размер экрана
    screen = pygame.display.set_mode(size)  # Создаем окно
    pygame.display.set_caption("Битва в космосе")  # Устанавливаем заголовок

    start_screen()

    main = MainScene(game_settings, screen, clock)

    main.loop()

    # По завершении главного игрового цикла выходим из игры
    pygame.quit()
