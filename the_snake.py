from random import choice, randint
import pygame

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
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет камня
STONE_COLOR = (128, 128, 128)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self):
        """Метод для инициализации базовых атрибутов объекта"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод для отрисовки объекта на игровом поле"""
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним
    """

    def __init__(self):
        """Метод для инициализации атрибутов объекта класса Apple"""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод для установки случайного положения яблока на игровом поле"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def draw(self):
        """Метод для отрисовки яблока на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий камень и действия с ним
    """

    def __init__(self):
        """Метод для инициализации атрибутов объекта класса Stone"""
        self.body_color = STONE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод для установки случайного положения камня на игровом поле"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def draw(self):
        """Метод для отрисовки камня на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение
    """

    def __init__(self):
        """Метод для инициализации атрибутов объекта класса Snake"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.position = self.positions[0]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод для обновления направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для обновления позиции змейки"""
        x, y = self.get_head_position()
        dx, dy = self.direction
        dx *= GRID_SIZE
        dy *= GRID_SIZE
        new_head = (x + dx) % SCREEN_WIDTH, (y + dy) % SCREEN_HEIGHT
        if new_head in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод для отрисовки змейки на игровой поверхности"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для получения позиции головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод для сбрасывания змейки в начальное состояние"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    """Функция main"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    while apple.position in snake.positions:
        apple.position = apple.randomize_position()
    stone = Stone()
    while (stone.position in snake.positions
            or stone.position == apple.position):
        stone.position = stone.randomize_position()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position()
            while (apple.position in snake.positions
                    or apple.position == stone.position):
                apple.position = apple.randomize_position()
            snake.length += 1
        if snake.get_head_position() == stone.position:
            snake.reset()
            stone.position = stone.randomize_position()
            while (stone.position in snake.positions
                    or stone.position == apple.position):
                stone.position = stone.randomize_position()
        snake.move()
        snake.draw()
        apple.draw()
        stone.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
