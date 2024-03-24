from random import randint, random

import pygame
from spacebattle.explosion import Explosion
from spacebattle.reward import Reward
from spacebattle.ship import Ship
from spacebattle.simplealienship import SimpleAlienShip
from spacebattle.strongalienship import StrongAlienShip
from spacebattle.stars import Stars


class MainScene:

    def __init__(self, game_settings, screen, clock):

        self.clock = clock

        self.bullets = []  # Пули

        self.game_settings = game_settings
        self.screen = screen

        # Звезды
        self.stars = Stars(game_settings, screen)

        # Корабль игрока
        self.player_ship = Ship(game_settings, screen, self)

        # Корабли пришельцев
        self.aliens = []
        self.alien_delay = 90  # Через сколько кадров появляется вражеский корабль
        self.alien_frames_spend = 0  # Сколько кадров прошло с появления предыдущего корабля

        # Взрыв
        self.explosions = pygame.sprite.Group()

        # Жизни
        self.lives_pos_x = 20
        self.lives_pos_y = 20
        self.lives = game_settings.initial_lives  # Количество жизней

        # Очки в игре
        self.scores = 0
        self.scores_font = pygame.font.SysFont('arialblack', 48)  # Шрифт для очков в игре
        self.scores_pos_x_right = game_settings.screen_width - 20
        self.scores_pos_y = 10

        # Финальная надпись
        self.game_over_font = pygame.font.SysFont('arialblack', 48)  # Шрифт для финальной надписи
        self.game_over_img = self.game_over_font.render("Игра окончена", True, (232, 232, 232))
        self.game_over_scores_img = self.scores_font.render("Ваши очки:", True, (255, 127, 39))
        self.game_over_final_message_img = self.scores_font.render("Рекорд:", True, (232, 232, 232))
        self.game_over_new_high_scores_img = self.scores_font.render("Новый рекорд!!!", True, (240, 240, 39))


        self.rewards = pygame.sprite.Group()

    def loop(self):
        # Цикл, в котором рисуется кадр

        done = False  # Признак того, что нужно выходить из основного цикла
        game_over = False

        while not done:

            self.stars.update()

            if not game_over:
                # Обработка событий
                for event in pygame.event.get():
                    # Выход из программы
                    if event.type == pygame.QUIT:
                        done = True

                    # Обрабатываем события дочерних объектов
                    self.player_ship.handle_event(event)

                # ***** Изменяем состояние дочерних объектов *****

                # ***** корабли пришельцев *****
                for al in self.aliens.copy():
                    al.update()
                    # сдвигаем все корабли пришельцев вниз
                    # Удаляем вражеские корабли вышедшие за экран
                    if al.has_removed():
                        self.aliens.remove(al)
                        # Если вражеский корабль вылетел за экран,
                        # уменьшаем количество жизней
                        self.lives -= 1
                        if self.lives <= 0:
                            game_over = True
                            # Определяем рекорд
                            try:
                                record_file = open('record.txt', 'r')
                            except FileNotFoundError:
                                record = 0
                            else:
                                try:
                                    record = int(record_file.readline().strip())
                                except:
                                    record = 0
                                record_file.close()

                            if record >= self.scores:
                                self.game_over_final_message_img = self.scores_font.render("Рекорд: " + str(record),
                                                                                           True, (232, 232, 232))
                            else:
                                self.game_over_final_message_img = self.game_over_new_high_scores_img
                                try:
                                    record_file = open('record.txt', 'w')
                                except:
                                    pass
                                else:
                                    try:
                                        print(self.scores, file=record_file)
                                    except:
                                        pass
                                    record_file.close()

                # увеличиваем счетчик кадров, прошедших
                # с появления последнего нового корабля
                self.alien_frames_spend += 1

                if self.alien_frames_spend == round(self.alien_delay):
                    # Добавляем новый корабль
                    if random() >= self.game_settings.strong_ship_probability:
                        self.aliens.append(SimpleAlienShip(self.game_settings, self.screen, self,
                                                           randint(SimpleAlienShip.half_width,
                                                                   self.game_settings.screen_width -
                                                                   SimpleAlienShip.half_width), 0))
                    else:
                        self.aliens.append(StrongAlienShip(self.game_settings, self.screen, self,
                                                           randint(SimpleAlienShip.half_width,
                                                                   self.game_settings.screen_width -
                                                                   SimpleAlienShip.half_width), 0))

                    self.alien_frames_spend = 0

                # ***** Снаряды *****
                for bul in self.bullets.copy():
                    # Вычисляем новое положение снарядов
                    bul.update()
                    # Удаляем снарды, вышедшие за экран
                    if bul.has_removed():
                        self.bullets.remove(bul)

                # Определяем столкновени снарядов и кораблей противника
                for al in self.aliens.copy():
                    for bul in self.bullets.copy():
                        al.rect.centerx = al.x
                        al.rect.bottom = round(al.y)
                        bullet_rect = bul.rect
                        bullet_rect.centerx = bul.x
                        bullet_rect.bottom = round(bul.y)

                        # Обрабатываем столкновение корабля с пулей
                        if al.rect.colliderect(bullet_rect):
                            al.collision(bul)
                            break

                # Вычисляем количество оставшихся кадров и фазу взрыва
                for expl in self.explosions.sprites():
                    expl.update()

                # Изменяем положение призов
                for rew in self.rewards.sprites():
                    rew.update()

                self.player_ship.update()  # Корабль игрока

                # Определяем встречу корабля с призами
                for rew in self.rewards.sprites():
                    rew.rect.centerx = round(rew.x)
                    rew.rect.bottom = round(rew.y)

                    if self.player_ship.rect.colliderect(rew.rect):
                        self.player_ship.set_bullet_factory(rew.bullet_factory)
                        rew.play_get_sound()
                        self.rewards.remove(rew)

                # Усложняем игру
                if self.alien_delay > self.game_settings.frames_per_second:
                    self.alien_delay -= 0.0001
                self.game_settings.strong_ship_probability += 0.00001

            # ***** Формируем изобржние *****
            self.blit_me()

            if game_over:
                # Обработка событий
                for event in pygame.event.get():
                    # Выход из программы
                    if event.type == pygame.QUIT:
                        done = True

                # Выводим финальную надпись
                scores_img = self.scores_font.render(str(self.scores),
                                                     True, (255, 127, 39))
                gm_rect = self.game_over_img.get_rect()
                gs_rect = self.game_over_scores_img.get_rect()
                sc_rect = scores_img.get_rect()
                cent_x = self.screen.get_width() // 2
                gm_rect.centerx = cent_x
                gm_rect.centery = self.screen.get_height() * 1 // 10
                gs_rect.centerx = cent_x
                gs_rect.centery = self.screen.get_height() * 3 // 10
                sc_rect.centerx = cent_x
                sc_rect.top = gs_rect.bottom + 20
                self.screen.blit(self.game_over_img, gm_rect)
                self.screen.blit(self.game_over_scores_img, gs_rect)
                self.screen.blit(scores_img, sc_rect)

                rc_rect = self.game_over_final_message_img.get_rect()
                rc_rect.centerx = cent_x
                rc_rect.centery = self.screen.get_height() * 6 // 10
                self.screen.blit(self.game_over_final_message_img, rc_rect)

            # Выводим новый кадр
            pygame.display.flip()
            self.clock.tick(self.game_settings.frames_per_second)

    def blit_me(self):
        # Выводим фон
        self.screen.fill((50, 50, 50))

        # Рисуем звезды
        self.stars.blit_me()

        # Рисуем вражеские корабли
        for al in self.aliens:
            al.blit_me()

        # Рисуем пули
        for bul in self.bullets:
            bul.blit_me()

        # Рисуем свой корабль
        self.player_ship.blit_me()

        # Рисуем взрывы
        for expl in self.explosions:
            expl.blit_me()

        # Рисуем призы
        for rew in self.rewards:
            rew.blit_me()

        # Рисуем количество жизней
        self.player_ship.blit_me_at(self.lives_pos_x, self.lives_pos_y,
                                    self.lives)

        # Выводим очки
        scores_img = self.scores_font.render(str(self.scores),
                                             True, (255, 127, 39))
        scores_rect = scores_img.get_rect()
        scores_rect.right = self.scores_pos_x_right
        scores_rect.top = self.scores_pos_y
        self.screen.blit(scores_img, scores_rect)

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def remove_alien(self, alien=None, bullet=None):
        if alien:
            self.aliens.remove(alien)
            self.explosions.add(Explosion(self.game_settings, self.screen,
                                          alien.rect.centerx,
                                          alien.rect.centery))
            # Даем очки за сбитый корабль
            self.scores += alien.ship_scores
            # Создаем награду
            if random() < alien.reward_probability:
                self.rewards.add(Reward.get_random_reward(self.game_settings,
                                                          self.screen, alien.x, alien.y))

        if bullet and not bullet.unremovable:
            self.bullets.remove(bullet)
