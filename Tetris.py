import random
import sqlite3
import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 24

# Подключаем базу данных
con = sqlite3.connect('scores.db')
cur = con.cursor()

# Размеры окна
SCREEN = WIDTH, HEIGHT = 300, 500

CELLSIZE = 20
ROWS = (HEIGHT - 120) // CELLSIZE
COLS = WIDTH // CELLSIZE

# Цвета
BLACK = (10, 10, 10)
BLUE = (20, 15, 100)
RED = (255, 100, 130)
WHITE = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode(SCREEN)
pygame.display.set_caption("Тетрис")

# Загрузка изображений
background_image = pygame.image.load('screensaver.png')

img1 = pygame.image.load('Assets/block1.png')
img2 = pygame.image.load('Assets/block2.png')
img3 = pygame.image.load('Assets/block3.png')
img4 = pygame.image.load('Assets/block4.png')

Assets = {
    1: img1,
    2: img2,
    3: img3,
    4: img4
}

# Шрифты для текста
font = pygame.font.Font(None, 30)
font1 = pygame.font.Font('Fonts/BrunoAceSC-Regular.ttf', 50)
font2 = pygame.font.SysFont('cursive', 25)

# Функция для отображения текста
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
                running = False  # Переход к следующему экрану при нажатии на пробел

    # Отображение фона
    screen.blit(background_image, (0, 0))

    # Отображение текста
    draw_text('Нажмите пробел,', font, WHITE, screen, 67, 350)
    draw_text('чтобы начать игру', font, WHITE, screen, 60, 380)

    # Обновление экрана
    pygame.display.flip()

win = pygame.display.set_mode(SCREEN)


class Tetramino:
    # matrix
    # 0   1   2   3
    # 4   5   6   7
    # 8   9   10  11
    # 12  13  14  15

    # Индексы ячеек, которые занимают блоки в данной матрице
    FIGURES = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }

    TYPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]
        self.color = random.randint(1, 4)
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)


class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.board = [[0 for j in range(cols)] for i in range(rows)]
        self.next = None
        self.gameover = False
        self.new_figure()
        try:
            cur.execute("""CREATE TABLE best (
    best_score INTEGER
);""")
            cur.execute("""INSERT INTO best (
                     best_score
                 )
                 VALUES (
                     0
                 );""")
        except:
            pass
        cur.execute("""select best_score from best""")
        self.best_score = cur.fetchall()[0][0]

    # Функция для отрисовки сетки
    def draw_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(win, WHITE, (0, CELLSIZE * i), (WIDTH, CELLSIZE * i))
        for j in range(self.cols):
            pygame.draw.line(win, WHITE, (CELLSIZE * j, 0), (CELLSIZE * j, HEIGHT - 120))

    # Функция для выбора новой фигуры
    def new_figure(self):
        if not self.next:
            self.next = Tetramino(5, 0)
        self.figure = self.next
        self.next = Tetramino(5, 0)

    # Функция для проверки пересекаются ли фигуры
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.rows - 1 or \
                            j + self.figure.x > self.cols - 1 or \
                            j + self.figure.x < 0 or \
                            self.board[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    # Функция для очистки заполненной линии
    def remove_line(self):
        rerun = False
        for y in range(self.rows - 1, 0, -1):
            is_full = True
            for x in range(0, self.cols):
                if self.board[y][x] == 0:
                    is_full = False
            if is_full:
                del self.board[y]
                self.board.insert(0, [0 for i in range(self.cols)])
                self.score += 1
                rerun = True
        if rerun:
            self.remove_line()

    # Функция для остановки падения фигуры
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.remove_line()
        self.new_figure()
        if self.intersects():
            self.gameover = True

    # Функция для мгновенного спуска фигуры
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    # Функция для ускорения падения фигуры
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    # Функция для перемещения фигуры по горизонтали
    def go_side(self, dx):
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx

    # Функция для поворота фигуры
    def rotate(self):
        rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = rotation


counter = 0
move_down = False
can_move = True

tetris = Tetris(ROWS, COLS)

# Основной игровой цикл
running = True
while running:
    win.fill(BLACK)

    counter += 1
    if counter >= 10000:
        counter = 0

    if can_move:
        if counter % (FPS // 2) == 0 or move_down:
            if not tetris.gameover:
                tetris.go_down()

    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if can_move and not tetris.gameover:
                if event.key == pygame.K_LEFT:
                    tetris.go_side(-1)

                if event.key == pygame.K_RIGHT:
                    tetris.go_side(1)

                if event.key == pygame.K_UP:
                    tetris.rotate()

                if event.key == pygame.K_DOWN:
                    move_down = True

                if event.key == pygame.K_SPACE:
                    tetris.go_space()

            if event.key == pygame.K_r:
                tetris.__init__(ROWS, COLS)

            if event.key == pygame.K_p:
                can_move = not can_move

            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                move_down = False

    # отрисовка упавших фигур
    for x in range(ROWS):
        for y in range(COLS):
            if tetris.board[x][y] > 0:
                val = tetris.board[x][y]
                img = Assets[val]
                win.blit(img, (y * CELLSIZE, x * CELLSIZE))
                pygame.draw.rect(win, BLACK, (y * CELLSIZE, x * CELLSIZE,
                                              CELLSIZE, CELLSIZE), 1)

    # отрисовка падающих фигур
    if tetris.figure:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetris.figure.image():
                    img = Assets[tetris.figure.color]
                    x = CELLSIZE * (tetris.figure.x + j)
                    y = CELLSIZE * (tetris.figure.y + i)
                    win.blit(img, (x, y))
                    pygame.draw.rect(win, BLACK, (x, y, CELLSIZE, CELLSIZE), 1)

    # конец игры

    if tetris.gameover:
        rect = pygame.Rect((50, 140, WIDTH - 100, HEIGHT - 350))
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, RED, rect, 2)

        over = font2.render('Game Over', True, WHITE)
        msg1 = font2.render('Press R to restart', True, RED)
        msg2 = font2.render('Press Q to quit', True, RED)

        win.blit(over, (rect.centerx - over.get_width() / 2, rect.y + 20))
        win.blit(msg1, (rect.centerx - msg1.get_width() / 2, rect.y + 80))
        win.blit(msg2, (rect.centerx - msg2.get_width() / 2, rect.y + 110))

        if tetris.score > tetris.best_score:
            cur.execute(f"""UPDATE best
   SET best_score = {tetris.score}
 WHERE best_score = {tetris.best_score};
""")

    # интерфейс

    pygame.draw.rect(win, BLUE, (0, HEIGHT - 120, WIDTH, 120))
    if tetris.next:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetris.next.image():
                    img = Assets[tetris.next.color]
                    x = CELLSIZE * (tetris.next.x + j - 4)
                    y = HEIGHT - 100 + CELLSIZE * (tetris.next.y + i)
                    win.blit(img, (x, y))

    scoreimg = font1.render(f'{tetris.score}', True, WHITE)
    levelimg = font2.render(f'Best score : {tetris.best_score}', True, WHITE)
    win.blit(scoreimg, (250 - scoreimg.get_width() // 2, HEIGHT - 110))
    win.blit(levelimg, (220 - levelimg.get_width() // 2, HEIGHT - 30))

    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT - 120), 2)
    clock.tick(FPS)
    pygame.display.update()

con.commit()
con.close()
pygame.quit()
