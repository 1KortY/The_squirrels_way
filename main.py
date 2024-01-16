import os
import sys
import pygame


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
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = load_image('bg_space.jpg')  # смена фона начального экрана
    screen.blit(fon, (0, -12))
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


def start_game():
    screen.blit(load_image('bg_space.jpg'), (0, -12))
    generate_level(load_level('level_1.txt'))
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

    tile = 50

    start_screen()

    player, level_x, level_y = generate_level(load_level('level_1.txt'))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

        screen.blit(load_image('bg_space.jpg'), (0, -12))
        tiles_group.draw(screen)
        player_group.draw(screen)

        # обработка остальных событий

        #all_sprites.draw(screen)

        # формирование кадра
        # ...
        pygame.display.flip()  # смена кадра
        # изменение игрового мира
        # ...
        # временная задержка
        clock.tick(fps)