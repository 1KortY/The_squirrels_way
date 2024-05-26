import os
import sys
import pygame
import time
import menu
from button import ImageButton

keys = 0
tile = 80
cur_lvl = 1
player = [1, 2, 3, 4]
door = [1, 2, 3, 4]
key1 = [1, 2, 3, 4]
key2 = [1, 2, 3, 4]
key3 = [1, 2, 3, 4]
key4 = [1, 2, 3, 4]
key5 = [1, 2, 3, 4]
time_3 = 22
time_4 = 33
g = []
k = ['$', '*', '(', ')', '+']
end = False


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.x = 0
        self.y = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.x
        obj.rect.y += self.y

    # позиционировать камеру на объекте target
    def update(self, target, n=0):
        if n == 1:
            self.x = -(target.rect.x + target.rect.w // 2 - width // 2)
        else:
            self.x = -(target.rect.x + target.rect.w // 2 - width // 2)
            self.y = -(target.rect.y + target.rect.h // 2 - height // 2)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def level_completed():
    global g
    global end
    if end:
        end = False
        restart_button = ImageButton(width / 2 - 300, 480, 252, 74, 'Начать заново', 'data/button.png',
                                     'data/button_hover.png', 'data/click.mp3')
        mback_button = ImageButton(width / 2 + 20, 480, 252, 74, 'В меню', 'data/button.png',
                                   'data/button_hover.png', 'data/click.mp3')
        running = True
        while running:
            screen.blit(load_image('bg_space.jpg'), (0, -12))
            font = pygame.font.Font(None, 72)
            text_surface = font.render("Уровень не пройден :(", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width / 2, 100))
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, (0, 1, 51), (width / 2 - 350, 130, 700, 500), 0)
            pygame.draw.rect(screen, (150, 0, 0), (width / 2 - 350, 130, 700, 500), 8)
            picture = pygame.image.load('data/game_over.png')
            picture_rect = picture.get_rect(bottomright=(882, 476))
            screen.blit(picture, picture_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu.fade()
                        start_screen()
                if event.type == pygame.USEREVENT and event.button == mback_button:
                    menu.fade()
                    return start_screen()
                if event.type == pygame.USEREVENT and event.button == restart_button:
                    menu.fade()
                    return start_game(cur_lvl)
                for btn in [restart_button, mback_button]:
                    btn.handle_event(event)
            for btn in [restart_button, mback_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)
            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x - 2, y - 2))
            pygame.display.flip()
    elif cur_lvl == 4:
        mback_button = ImageButton(width / 2 - 126, 480, 252, 74, 'В меню', 'data/button.png',
                                   'data/button_hover.png', 'data/click.mp3')
        g.append(cur_lvl)
        running = True
        while running:
            screen.blit(load_image('bg_space.jpg'), (0, -12))

            font = pygame.font.Font(None, 72)
            text_surface = font.render("Уровень пройден!", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width / 2, 100))
            screen.blit(text_surface, text_rect)

            pygame.draw.rect(screen, (0, 1, 51), (width / 2 - 350, 130, 700, 500), 0)
            pygame.draw.rect(screen, (150, 0, 0), (width / 2 - 350, 130, 700, 500), 8)
            picture = pygame.image.load('data/level_end.png')
            picture_rect = picture.get_rect(bottomright=(882, 476))
            screen.blit(picture, picture_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu.fade()
                        start_screen()

                if event.type == pygame.USEREVENT and event.button == mback_button:
                    menu.fade()
                    return start_screen()

                for btn in [mback_button]:
                    btn.handle_event(event)

            for btn in [mback_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x - 2, y - 2))

            pygame.display.flip()
    else:
        resume_button = ImageButton(width / 2 - 300, 480, 252, 74, 'След. уровень', 'data/button.png',
                                    'data/button_hover.png', 'data/click.mp3')
        mback_button = ImageButton(width / 2 + 20, 480, 252, 74, 'В меню', 'data/button.png',
                                   'data/button_hover.png', 'data/click.mp3')
        g.append(cur_lvl)
        running = True
        while running:
            screen.blit(load_image('bg_space.jpg'), (0, -12))
            font = pygame.font.Font(None, 72)
            text_surface = font.render("Уровень пройден!", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width / 2, 100))
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, (0, 1, 51), (width / 2 - 350, 130, 700, 500), 0)
            pygame.draw.rect(screen, (150, 0, 0), (width / 2 - 350, 130, 700, 500), 8)
            picture = pygame.image.load('data/level_end.png')
            picture_rect = picture.get_rect(bottomright=(882, 476))
            screen.blit(picture, picture_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu.fade()
                        start_screen()
                if event.type == pygame.USEREVENT and event.button == mback_button:
                    menu.fade()
                    return start_screen()
                if event.type == pygame.USEREVENT and event.button == resume_button:
                    menu.fade()
                    return start_game(cur_lvl + 1)
                for btn in [resume_button, mback_button]:
                    btn.handle_event(event)
            for btn in [resume_button, mback_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)
            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x - 2, y - 2))
            pygame.display.flip()


def level_menu():
    level1_button = ImageButton(width / 2 - (252 / 2), 150, 252, 74, 'Уровень 1', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')
    level2_button = ImageButton(width / 2 - (252 / 2), 250, 252, 74, 'Уровень 2', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')
    level3_button = ImageButton(width / 2 - (252 / 2), 350, 252, 74, 'Уровень 3', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')
    level4_button = ImageButton(width / 2 - (252 / 2), 450, 252, 74, 'Уровень 4', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')
    back_button = ImageButton(width / 2 - (252 / 2), 550, 252, 74, 'Назад', 'data/button.png',
                              'data/button_hover.png', 'data/click.mp3')

    running = True
    while running:
        screen.blit(load_image('bg_space.jpg'), (0, -12))
        for i in g:
            pygame.draw.line(screen, (0, 250, 0), (width / 2 + 130, 60 + 100 * i), (width / 2 + 145, 40 + 100 * i + 74),
                             7)
            pygame.draw.line(screen, (0, 250, 0), (width / 2 + 145, 40 + 100 * i + 74),
                             (width / 2 + 165, 50 + 100 * i - 20), 7)

        font = pygame.font.Font(None, 72)
        text_surface = font.render("Выберите уровень", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                menu.fade()
                running = False
                return start_screen()

            if event.type == pygame.USEREVENT and event.button == level1_button:
                menu.fade()
                return start_game(1)

            if event.type == pygame.USEREVENT and event.button == level2_button:
                menu.fade()
                return start_game(2)

            if event.type == pygame.USEREVENT and event.button == level3_button:
                menu.fade()
                return start_game(3)

            if event.type == pygame.USEREVENT and event.button == level4_button:
                menu.fade()
                return start_game(4)

            for btn in [level1_button, level2_button, level3_button, level4_button, back_button]:
                btn.handle_event(event)

        for btn in [level1_button, level2_button, level3_button, level4_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, number):
        super().__init__(tiles_group[number - 1], all_sprites[number - 1])
        self.x = pos_x
        self.y = pos_y
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile * pos_x, tile * (pos_y * 0.55))
        if tile_type == 'key':
            self.rect = self.rect.move(23, -20)
        if tile_type == 'nut':
            self.rect = self.rect.move(15, -5)
        if tile_type == 'door' or tile_type == 'door_open':
            self.rect = self.rect.move(10, -15)

    def lifting_key(self):
        self.rect = self.rect.move(0, -1000)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, number):
        super().__init__(player_group[number - 1], all_sprites[number - 1])
        self.number = number
        self.x = pos_x
        self.y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(tile * pos_x + 10, tile * (pos_y * 0.55) - 40)

    def move_up(self):
        if can_move(self.x, self.y - 1, self.number):
            x, y = tile * self.x + 10, tile * ((self.y - 1) * 0.55 - 40)
            self.y -= 1
            screen.blit(self.image, (x, y))
            for i in range(11):
                screen.blit(load_image('bg_space.jpg'), (0, -12))
                inscriptions()

                # изменяем ракурс камеры
                camera.update(player[cur_lvl - 1])
                # обновляем положение всех спрайтов
                for sprite in all_sprites[cur_lvl - 1]:
                    camera.apply(sprite)

                self.rect = self.rect.move(0, -4)

                tiles_group[cur_lvl - 1].draw(screen)
                player_group[cur_lvl - 1].draw(screen)

                pygame.display.flip()

    def move_down(self):
        if can_move(self.x, self.y + 1, self.number):
            x, y = tile * self.x + 10, tile * ((self.y + 1) * 0.55 - 40)
            self.y += 1
            screen.blit(self.image, (x, y))
            for i in range(11):
                screen.blit(load_image('bg_space.jpg'), (0, -12))
                inscriptions()

                # изменяем ракурс камеры
                camera.update(player[cur_lvl - 1])
                # обновляем положение всех спрайтов
                for sprite in all_sprites[cur_lvl - 1]:
                    camera.apply(sprite)

                self.rect = self.rect.move(0, 4)

                tiles_group[cur_lvl - 1].draw(screen)
                player_group[cur_lvl - 1].draw(screen)

                pygame.display.flip()

    def move_right(self):
        if can_move(self.x + 1, self.y, self.number):
            x, y = tile * (self.x + 1) + 10, tile * (self.y * 0.55) - 40
            self.x += 1
            screen.blit(self.image, (x, y))
            x = -3
            y = 0
            for i in range(16):
                screen.blit(load_image('bg_space.jpg'), (0, -12))
                inscriptions()

                # изменяем ракурс камеры
                camera.update(player[cur_lvl - 1], 1)
                # обновляем положение всех спрайтов
                for sprite in all_sprites[cur_lvl - 1]:
                    camera.apply(sprite)

                if i == 1:
                    y = -1
                elif i == 9:
                    y = 1

                self.rect = self.rect.move(5, y * (x ** 2))
                x += 0.375

                tiles_group[cur_lvl - 1].draw(screen)
                player_group[cur_lvl - 1].draw(screen)

                pygame.display.flip()

    def move_left(self):
        if can_move(self.x - 1, self.y, self.number):
            x, y = tile * (self.x - 1) + 10, tile * (self.y * 0.55) - 40
            self.x -= 1
            screen.blit(self.image, (x, y))
            x = 3
            y = 0
            for i in range(16):
                screen.blit(load_image('bg_space.jpg'), (0, -12))
                inscriptions()

                # изменяем ракурс камеры
                camera.update(player[cur_lvl - 1], 1)
                # обновляем положение всех спрайтов
                for sprite in all_sprites[cur_lvl - 1]:
                    camera.apply(sprite)

                if i == 1:
                    y = -1
                elif i == 9:
                    y = 1

                self.rect = self.rect.move(-5, y * (x ** 2))
                x -= 0.375

                tiles_group[cur_lvl - 1].draw(screen)
                player_group[cur_lvl - 1].draw(screen)

                pygame.display.flip()


def can_move(x, y, number):
    global keys
    if load_level(f'level_{cur_lvl}.txt')[y][x] == '#' or \
            load_level(f'level_{cur_lvl}.txt')[y][x] == '@':
        return True
    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '$':
        if '$' in k:
            key1[number - 1].lifting_key()
            keys += 1
            k.remove('$')
        return True

    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '*':
        if '*' in k:
            key2[number - 1].lifting_key()
            keys += 1
            k.remove('*')
        return True

    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '(':
        if '(' in k:
            key3[number - 1].lifting_key()
            keys += 1
            k.remove('(')
        return True

    elif load_level(f'level_{cur_lvl}.txt')[y][x] == ')':
        if ')' in k:
            key4[number - 1].lifting_key()
            keys += 1
            k.remove(')')
        return True

    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '+':
        if '+' in k:
            key5[number - 1].lifting_key()
            keys += 1
            k.remove('+')
        return True

    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '%':
        if number == 1 and keys == 1:
            return True
        elif number == 2 and keys == 2:
            return True
        elif number == 3 and keys == 3:
            return True
        elif number == 4 and keys == 5:
            return True

    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '?':
        if number == 1 and keys == 1:
            door[number - 1].lifting_key()
        elif number == 2 and keys == 2:
            door[number - 1].lifting_key()
        elif number == 3 and keys == 3:
            door[number - 1].lifting_key()
        elif number == 4 and keys == 5:
            door[number - 1].lifting_key()
        return True

    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '&':
        level_completed()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    start_button = ImageButton(width / 2 - (252 / 2), 200, 252, 74, 'Играть', 'data/button.png',
                               'data/button_hover.png', 'data/click.mp3')
    level_button = ImageButton(width / 2 - (252 / 2), 300, 252, 74, 'Выбрать уровень', 'data/button.png',
                               'data/button_hover.png', 'data/click.mp3')
    exit_button = ImageButton(width / 2 - (252 / 2), 400, 252, 74, 'Выйти', 'data/button.png',
                              'data/button_hover.png', 'data/click.mp3')

    running = True
    while running:
        screen.blit(load_image('bg_space.jpg'), (0, -12))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("The squirrel's way", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(None, 40)
        text_surface = font.render("Благодаря ореху белка может выжить в космосе,", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 550))
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(None, 40)
        text_surface = font.render("поэтому задача взять орех.", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 600))
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(None, 20)
        text_surface = font.render("Все события в данной игре вымышленные,", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(920, 680))
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(None, 20)
        text_surface = font.render("сходство с реальными событиями случайно", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(920, 700))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if event.type == pygame.USEREVENT and event.button == start_button:
                menu.fade()
                return start_game(1)

            if event.type == pygame.USEREVENT and event.button == level_button:
                running = False
                menu.fade()
                level_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                terminate()

            for btn in [start_button, level_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, level_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, number):
    new_player, door, key_1, key_2, key_3, key_4, key_5 = None, None, None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile('meteor', x, y, number)

            elif level[y][x] == '@':
                Tile('meteor', x, y, number)
                new_player = Player(x, y, number)

            elif level[y][x] == '&':
                Tile('meteor', x, y, number)
                Tile('nut', x, y, number)

            elif level[y][x] == '$':
                Tile('meteor', x, y, number)
                key_1 = Tile('key', x, y, number)

            elif level[y][x] == '*':
                Tile('meteor', x, y, number)
                key_2 = Tile('key', x, y, number)

            elif level[y][x] == '(':
                Tile('meteor', x, y, number)
                key_3 = Tile('key', x, y, number)

            elif level[y][x] == ')':
                Tile('meteor', x, y, number)
                key_4 = Tile('key', x, y, number)

            elif level[y][x] == '+':
                Tile('meteor', x, y, number)
                key_5 = Tile('key', x, y, number)

            elif level[y][x] == '%':
                Tile('meteor', x, y, number)
                Tile('door_open', x, y, number)
                door = Tile('door', x, y, number)

            elif level[y][x] == '?':
                Tile('meteor', x, y, number)

    # вернем игрока, а также размер поля в клетках
    return new_player, door, key_1, key_2, key_3, key_4, key_5


def inscriptions():
    global end
    font = pygame.font.Font(None, 40)
    if cur_lvl == 1:
        text_surface = font.render(f"Собрано ключей: {keys}/1", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(900, 40))
        screen.blit(text_surface, text_rect)

        text_surface = font.render(f"Уровень 1", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(100, 40))
        screen.blit(text_surface, text_rect)

    elif cur_lvl == 2:
        text_surface = font.render(f"Собрано ключей: {keys}/2", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(900, 40))
        screen.blit(text_surface, text_rect)

        text_surface = font.render(f"Уровень 2", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(100, 40))
        screen.blit(text_surface, text_rect)

    elif cur_lvl == 3:
        global time_3
        text_surface = font.render(f"Собрано ключей: {keys}/3", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(900, 40))
        screen.blit(text_surface, text_rect)

        text_surface = font.render(f"Уровень 3", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(100, 40))
        screen.blit(text_surface, text_rect)

        time_3 -= 0.016
        text_surface = font.render(f"Осталось времени: {round(time_3, 2)}", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(x=350, y=27)
        screen.blit(text_surface, text_rect)

        if time_3 <= 0:
            time_3 = 22
            end = True
            return level_completed()

    elif cur_lvl == 4:
        global time_4
        text_surface = font.render(f"Собрано ключей: {keys}/5", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(900, 40))
        screen.blit(text_surface, text_rect)

        text_surface = font.render(f"Уровень 4", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(100, 40))
        screen.blit(text_surface, text_rect)

        time_4 -= 0.016
        text_surface = font.render(f"Осталось времени: {round(time_4, 2)}", True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(x=350, y=27)
        screen.blit(text_surface, text_rect)

        if time_4 <= 0:
            time_4 = 33
            end = True
            return level_completed()


def start_game(number):
    global cur_lvl
    global keys
    global player, door, key1, key2, key3, key4, key5
    global k
    k = ['$', '*', '(', ')', '+']
    keys = 0
    cur_lvl = number

    all_sprites_1.empty()
    all_sprites_2.empty()
    all_sprites_3.empty()
    all_sprites_4.empty()

    tiles_group_1.empty()
    tiles_group_2.empty()
    tiles_group_3.empty()
    tiles_group_4.empty()

    player_group_1.empty()
    player_group_2.empty()
    player_group_3.empty()
    player_group_4.empty()

    player_1, door_1, key1_1, key2_1, key3_1, key4_1, key5_1 = generate_level(load_level(f'level_1.txt'), 1)
    player_2, door_2, key1_2, key2_2, key3_2, key4_2, key5_2 = generate_level(load_level(f'level_2.txt'), 2)
    player_3, door_3, key1_3, key2_3, key3_3, key4_3, key5_3 = generate_level(load_level(f'level_3.txt'), 3)
    player_4, door_4, key1_4, key2_4, key3_4, key4_4, key5_4 = generate_level(load_level(f'level_4.txt'), 4)

    player = [player_1, player_2, player_3, player_4]
    door = [door_1, door_2, door_3, door_4]
    key1 = [key1_1, key1_2, key1_3, key1_4]
    key2 = [key2_1, key2_2, key2_3, key2_4]
    key3 = [key3_1, key3_2, key3_3, key3_4]
    key4 = [key4_1, key4_2, key4_3, key4_4]
    key5 = [key5_1, key5_2, key5_3, key5_4]

    screen.blit(load_image('bg_space.jpg'), (0, -12))

    inscriptions()

    all_sprites[number - 1].draw(screen)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("The squirrel's way")
    size = width, height = 1080, 720
    screen = pygame.display.set_mode(size)

    fps = 120  # количество кадров в секунду
    clock = pygame.time.Clock()

    # группы спрайтов
    all_sprites_1 = pygame.sprite.Group()
    all_sprites_2 = pygame.sprite.Group()
    all_sprites_3 = pygame.sprite.Group()
    all_sprites_4 = pygame.sprite.Group()

    tiles_group_1 = pygame.sprite.Group()
    tiles_group_2 = pygame.sprite.Group()
    tiles_group_3 = pygame.sprite.Group()
    tiles_group_4 = pygame.sprite.Group()

    player_group_1 = pygame.sprite.Group()
    player_group_2 = pygame.sprite.Group()
    player_group_3 = pygame.sprite.Group()
    player_group_4 = pygame.sprite.Group()

    tiles_group = [tiles_group_1, tiles_group_2, tiles_group_3, tiles_group_4]
    player_group = [player_group_1, player_group_2, player_group_3, player_group_4]
    all_sprites = [all_sprites_1, all_sprites_2, all_sprites_3, all_sprites_4]

    tile_images = {
        'meteor': load_image('asteroid.png'),
        'key': load_image('key.png'),
        'nut': load_image('nut.png'),
        'door': load_image('door.png'),
        'door_open': load_image('door_open.png')
    }
    player_image = load_image('player.png')
    cursor = load_image('cursor.png')

    start_screen()

    camera = Camera()

    running = True
    while running:
        screen.blit(load_image('bg_space.jpg'), (0, -12))
        inscriptions()

        # изменяем ракурс камеры
        camera.update(player[cur_lvl - 1])
        # обновляем положение всех спрайтов
        for sprite in all_sprites[cur_lvl - 1]:
            camera.apply(sprite)

        tiles_group[cur_lvl - 1].draw(screen)
        player_group[cur_lvl - 1].draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player[cur_lvl - 1].move_up()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player[cur_lvl - 1].move_left()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player[cur_lvl - 1].move_down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player[cur_lvl - 1].move_right()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.fade()
                    start_screen()

        pygame.display.flip()
        clock.tick(fps)
