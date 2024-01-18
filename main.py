import os
import sys
import pygame
import menu
from button import ImageButton


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
    resume_button = ImageButton(width / 2 - 300, 480, 252, 74, 'След. уровень', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')
    mback_button = ImageButton(width / 2 + 20, 480, 252, 74, 'В меню', 'data/button.png',
                               'data/button_hover.png', 'data/click.mp3')

    running = True
    while running:
        screen.blit(load_image('bg_space.jpg'), (0, -12))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("Уровень пройден", True, (255, 255, 255))
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
                start_screen()

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
    back_button = ImageButton(width / 2 - (252 / 2), 350, 252, 74, 'Назад', 'data/button.png',
                              'data/button_hover.png', 'data/click.mp3')

    running = True
    while running:
        screen.blit(load_image('bg_space.jpg'), (0, -12))

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

            if event.type == pygame.USEREVENT and event.button == level1_button:
                menu.fade()
                return start_game(1)

            if event.type == pygame.USEREVENT and event.button == level2_button:
                menu.fade()
                return start_game(2)

            # if event.type == pygame.USEREVENT and event.button == level3_button:
            #     fade()
            #     return main.start_game(2)

            for btn in [level1_button, level2_button, back_button]:
                btn.handle_event(event)

        for btn in [level1_button, level2_button, back_button]:
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

    def lifting_key(self):
        self.rect = self.rect.move(0, -1000)

    def open_door(self):



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, number):
        super().__init__(player_group[number - 1], all_sprites[number - 1])
        self.number = number
        self.x = pos_x
        self.y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(tile * pos_x, tile * (pos_y * 0.55))

    def move_up(self):
        if can_move(self.x, self.y - 1, self.number):
            print('up')
            x, y = tile * self.x, tile * ((self.y - 1) * 0.55)
            self.y -= 1
            screen.blit(self.image, (x, y))
            self.rect = self.rect.move(0, -tile * 0.55)

    def move_down(self):
        if can_move(self.x, self.y + 1, self.number):
            print('down')
            x, y = tile * self.x, tile * ((self.y + 1) * 0.55)
            self.y += 1
            screen.blit(self.image, (x, y))
            self.rect = self.rect.move(0, tile * 0.55)

    def move_right(self):
        if can_move(self.x + 1, self.y, self.number):
            print('right')
            x, y = tile * (self.x + 1), tile * (self.y * 0.55)
            self.x += 1
            screen.blit(self.image, (x, y))
            self.rect = self.rect.move(tile, 0)

    def move_left(self):
        if can_move(self.x - 1, self.y, self.number):
            print('left')
            x, y = tile * (self.x - 1), tile * (self.y * 0.55)
            self.x -= 1
            screen.blit(self.image, (x, y))
            self.rect = self.rect.move(-tile, 0)


def can_move(x, y, number):
    print(x, y)
    print(load_level(f'level_{cur_lvl}.txt')[y][x])
    if load_level(f'level_{cur_lvl}.txt')[y][x] == '#' or \
            load_level(f'level_{cur_lvl}.txt')[y][x] == '&' or \
            load_level(f'level_{cur_lvl}.txt')[y][x] == '@' or \
            load_level(f'level_{cur_lvl}.txt')[y][x] == '%':
        return True
    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '$':
        key1[number - 1].lifting_key()
        return True
    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '№':
        key2[number - 1].lifting_key()
        return True
    elif load_level(f'level_{cur_lvl}.txt')[y][x] == '?':
        door[number - 1].



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
    new_player, door, key_1, key_2, door_open = None, None, None, None, None
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
            elif level[y][x] == '№':
                Tile('meteor', x, y, number)
                key_2 = Tile('key', x, y, number)
            elif level[y][x] == '%':
                Tile('meteor', x, y, number)
                door = Tile('door', x, y, number)
                door_open = Tile('door', x, y, number)
                door_open.

    # вернем игрока, а также размер поля в клетках
    return new_player, door, key_1, key_2, door_open


def start_game(number):
    global cur_lvl
    screen.blit(load_image('bg_space.jpg'), (0, -12))
    cur_lvl = number
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

    tiles_group_1 = pygame.sprite.Group()
    tiles_group_2 = pygame.sprite.Group()
    tiles_group_3 = pygame.sprite.Group()

    player_group_1 = pygame.sprite.Group()
    player_group_2 = pygame.sprite.Group()
    player_group_3 = pygame.sprite.Group()

    tiles_group = [tiles_group_1, tiles_group_2, tiles_group_3]
    player_group = [player_group_1, player_group_2, player_group_3]
    all_sprites = [all_sprites_1, all_sprites_2, all_sprites_3]

    tile_images = {
        'meteor': load_image('asteroid.png'),
        'key': load_image('key.png'),
        'nut': load_image('nut.png'),
        'door': load_image('door.png'),
        #'door_open': load_image('door_open.png')
    }
    player_image = load_image('player.png')
    cursor = load_image('cursor.png')

    tile = 80

    cur_lvl = 1

    start_screen()

    player_1, door_1, key1_1, key2_1, door_open_1 = generate_level(load_level(f'level_1.txt'), 1)
    player_2, door_2, key1_2, key2_2, door_open_2 = generate_level(load_level(f'level_2.txt'), 2)
    #player_3, door_3, key1_3, key2_3, door_open_3 = generate_level(load_level(f'level_3.txt'), 3)

    player = [player_1, player_2]
    door = [door_1, door_2]
    key1 = [key1_1, key1_2]
    key2 = [key2_1, key2_2]
    door_open = [door_open_1, door_open_2]

    print(all_sprites)
    print(tiles_group)
    print(player_group)

    running = True
    while running:
        screen.blit(load_image('bg_space.jpg'), (0, -12))
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

        tiles_group[cur_lvl - 1].draw(screen)
        player_group[cur_lvl - 1].draw(screen)

        pygame.display.flip()
        # изменение игрового мира
        # ...
        # временная задержка
        clock.tick(fps)