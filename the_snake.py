from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (000, 000, 000)

# Цвет яблока
APPLE_COLOR = (000, 225, 000)

# Цвет змейки
SNAKE_COLOR = (130, 000, 250)

# Скорость движения змейки:
SPEED = 9

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка Айпери')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Родительский класс GameObject содержит 2 параметра; цвет и позицию объекта,
    и 1 метод - draw.
    """

    def __init__(self, body_color) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Класс draw по умолчанию pass."""
        raise NotImplementedError()


class Apple(GameObject):
    """Класс Apple наследует атрибуты родительсского класса GameObject."""

    def __init__(self, body_color):
        super().__init__(body_color)
        # self.position = self.randomize_position()

    def randomize_position(self, positions: list) -> None:
        """
        Метод randomize_position устанавливает
        случайное положение яблока на игровом поле.
        """
        # return ((randint(0, GRID_WIDTH) * GRID_SIZE),
        #         ((randint(0, GRID_HEIGHT) * GRID_SIZE)))
        while True:
            new_coordinat = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                        ((randint(0, GRID_HEIGHT - 1) * GRID_SIZE)))
            if new_coordinat not in positions:
                self.position = new_coordinat
                break



    def draw(self):
        """Метод draw класса Apple."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake наследует атрибуты родительсского класса GameObject."""

    def __init__(self, body_color):
        super().__init__(body_color)
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """
        Метод update_direction обновляет
        направления после нажатия на кнопку.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод move отвечает за обновление положения змейки в игре."""
        x, y = self.get_head_position()
        horizontal_move = self.direction[0]
        vertical_move = self.direction[1]
        new_step = (
            (x + horizontal_move * GRID_SIZE) % SCREEN_WIDTH,
            (y + vertical_move * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_step)

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop(-1)


    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Этот метод возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self, start_game=False):
        """Cбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        if start_game:
            self.direction = RIGHT
        else:
            self.direction = choice([UP, DOWN, LEFT, RIGHT])    


def handle_keys(game_object):
    """
    Функция, которая обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Тут опишите основную логику игры.
def main():
    """Функция содержит основной цикл игры."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    snake.reset(start_game=True)
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
