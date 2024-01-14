import os
import sys
import pygame
import random


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = load_image('bg_space.jpg')  # смена фона начального экрана
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.mouse or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return start_game()
        pygame.display.flip()
        clock.tick(fps)


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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]

        self.left = 20
        self.top = 20
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        y = self.left
        x = self.top
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size), self.board[i][j])
                x += self.cell_size
            x = self.top
            y += self.cell_size


def start_game():
    #screen.fill((0, 0, 0))
    screen.blit(load_image('bg_space.jpg'), (0, 0))
    player, level_x, level_y = generate_level(load_level('level_1.txt'))
    board = Board(level_x, level_y)
    board.set_view(0, 0, 50)
    screen.fill((0, 0, 0))
    board.render()
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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Название окна')
    size = width, height = 1080, 720
    screen = pygame.display.set_mode(size)

    fps = 120  # количество кадров в секунду
    clock = pygame.time.Clock()

    # основной персонаж
    player = None

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

    tile_width = tile_height = 50

    start_screen()

    # # создадим спрайт
    # balloon = pygame.sprite.Sprite(all_sprites)
    # # определим его вид
    # balloon.image = pygame.transform.scale(load_image('blue_balloon.jpg', -1), (50, 65))
    # # и размеры
    # balloon.rect = balloon.image.get_rect()
    # balloon.rect.x = 100
    # balloon.rect.y = 50

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # обработка остальных событий

        # all_sprites.draw(screen)

        # формирование кадра
        # ...
        pygame.display.flip()  # смена кадра
        # изменение игрового мира
        # ...
        # временная задержка
        clock.tick(fps)
