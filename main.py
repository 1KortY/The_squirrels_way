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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile * pos_x, tile * (pos_y * 0.57))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(tile * pos_x, tile * (pos_y * 0.57))

    def move_up(self):
        if can_move(self.x, self.y - 1):
            print('up')
            x, y = tile * self.x, tile * ((self.y - 1) * 0.57)
            self.y -= 1
            screen.blit(self.image, (x, y))
            self.rect = self.rect.move(0, -tile * 0.57)

    def move_down(self):
        if can_move(self.x, self.y + 1):
            print('down')
            x, y = tile * self.x, tile * ((self.y + 1) * 0.57)
            self.y += 1
            screen.blit(self.image, (x, y))
            self.rect = self.rect.move(0, tile * 0.57)

    def move_right(self):
        if can_move(self.x + 1, self.y):
            print('right')
            x, y = tile * (self.x + 1), tile * (self.y * 0.57)
            self.x += 1
            screen.blit(self.image, (x, y))
            self.rect = self.rect.move(tile, 0)

    def move_left(self):
        if can_move(self.x - 1, self.y):
            print('left')
            x, y = tile * (self.x - 1), tile * (self.y * 0.57)
            self.x -= 1
            screen.blit(self.image, (x, y))
            self.rect = self.rect.move(-tile, 0)


def can_move(x, y):
    print(load_level('level_1.txt')[y][x])
    if load_level('level_1.txt')[y][x] == '#' or \
            load_level('level_1.txt')[y][x] == '&' or \
            load_level('level_1.txt')[y][x] == '$' or \
            load_level('level_1.txt')[y][x] == '@':
        return True


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
                return start_game()

            if event.type == pygame.USEREVENT and event.button == level_button:
                menu.fade()
                menu.level_menu()

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


def start_game():
    screen.blit(load_image('bg_space.jpg'), (0, -12))
    generate_level(load_level(f'level_{cur_lvl}.txt'))
    # board = Board(screen, level_x, level_y)
    # board.set_view(0, 0, 50)
    # board.render()
    all_sprites.draw(screen)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile('meteor', x, y)
            elif level[y][x] == '@':
                Tile('meteor', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '&':
                Tile('meteor', x, y)
                Tile('nut', x, y)
            elif level[y][x] == '$':
                Tile('meteor', x, y)
                Tile('key', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("The squirrel's way")
    size = width, height = 1080, 720
    screen = pygame.display.set_mode(size)

    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    tile_images = {
        'meteor': load_image('asteroid.jpg'),
        'empty': load_image('blue_balloon.jpg'),
        'key': load_image('key.png'),
        'nut': load_image('nut.jpg')
    }
    player_image = load_image('player.jpg')
    cursor = load_image('cursor.png')

    tile = 50

    cur_lvl = 1

    start_screen()

    player, level_x, level_y = generate_level(load_level('level_1.txt'))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.move_up()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.move_left()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.move_down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.move_right()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.fade()
                    start_screen()

        screen.blit(load_image('bg_space.jpg'), (0, -12))
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        # изменение игрового мира
        # ..
        # временная задержка
        clock.tick(fps)