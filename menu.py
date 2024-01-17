import pygame
import sys
from button import ImageButton

pygame.init()

WIDTH, HEIGHT = 1080, 720
MAX_FPS = 60;

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Menu')
main_background = pygame.image.load('data/bg_space.jpg')
clock = pygame.time.Clock()
cursor = pygame.image.load('data/cursor.png')
pygame.mouse.set_visible(False)


def main_menu():
    start_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, 'Играть', 'data/button.png',
                               'data/button_hover.png', 'data/click.mp3')
    level_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, 'Выбрать уровень', 'data/button.png',
                               'data/button_hover.png', 'data/click.mp3')
    exit_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, 'Выйти', 'data/button.png',
                              'data/button_hover.png', 'data/click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, -300))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("The squirrel's way", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_button:
                fade()
                new_game()

            if event.type == pygame.USEREVENT and event.button == level_button:
                fade()
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [start_button, level_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, level_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


def settings_menu():
    level1_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, 'Уровень 1', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')
    level2_button = ImageButton(WIDTH / 2 - (252 / 2), 250, 252, 74, 'Уровень 2', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')
    level3_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, 'Назад', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, -10))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("ВЫБОР УРОВНЯ", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == level3_button:
                fade()
                running = False

            for btn in [level1_button, level2_button, level3_button]:
                btn.handle_event(event)

        for btn in [level1_button, level2_button, level3_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


def new_game():
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, 'Назад', 'data/button.png',
                              'data/button_hover.png', 'data/click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(main_background, (0, -10))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("Первый уровень", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False

            for btn in [back_button]:
                btn.handle_event(event)

        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


def fade():
    running = True
    fade_alpha = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main_menu()