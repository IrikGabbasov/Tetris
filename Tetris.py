import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 24


BLACK = (21, 24, 29) # Цвета
BLUE = (31, 25, 76)
RED = (252, 91, 122)
WHITE = (255, 255, 255)


font1 = pygame.font.Font('Fonts/Alternity-8w7J.ttf', 50)
font2 = pygame.font.SysFont('cursive', 25)
# Размеры окна
screen_width = 700
screen_height = 600

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Тетрис")

# Загрузка изображения
background_image = pygame.image.load('screensaver.png')

# Шрифт для текста
font = pygame.font.Font(None, 36)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Цикл заставки
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False # Переход к следующему экрану при нажатии на пробел

    # Отображение фона
    screen.blit(background_image, (0, 0))

    # Отображение текста
    draw_text('Нажмите пробел, чтобы начать игру', font, (255, 255, 255), screen, 100, 500)

    # Обновление экрана
    pygame.display.flip()


SCREEN = WIDTH, HEIGHT = 300, 500
win = pygame.display.set_mode(SCREEN)

CELLSIZE = 20
ROWS = (HEIGHT - 120) // CELLSIZE
COLS = WIDTH // CELLSIZE


running = True
while running:
    win.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    scoreimg = font1.render(f'{1}', True, WHITE)
    levelimg = font2.render(f'Total score : {2}', True, WHITE)
    win.blit(scoreimg, (250 - scoreimg.get_width() // 2, HEIGHT - 110))
    win.blit(levelimg, (220 - levelimg.get_width() // 2, HEIGHT - 30))

    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT - 120), 2)
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()