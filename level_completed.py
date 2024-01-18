def level_completed():
    resume_button = ImageButton(WIDTH / 2 - 300, 480, 252, 74, 'След. уровень', 'data/button.png',
                                'data/button_hover.png', 'data/click.mp3')
    mback_button = ImageButton(WIDTH / 2 + 20, 480, 252, 74, 'В меню', 'data/button.png',
                               'data/button_hover.png', 'data/click.mp3')

    running = True
    while running:
        screen.blit(main_background, (0, -12))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("Уровень пройден", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0, 1, 51), (WIDTH / 2 - 350, 130, 700, 500), 0)
        pygame.draw.rect(screen, (150, 0, 0), (WIDTH / 2 - 350, 130, 700, 500), 8)
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

            for btn in [resume_button, mback_button]:
                btn.handle_event(event)

        for btn in [resume_button, mback_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()