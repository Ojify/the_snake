import random
import pygame

# --- КОНСТАНТЫ (требуются для тестов) ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Инициализация Pygame и глобальные переменные (требуются для тестов)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """Инициализирует позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализирует яблоко красного цвета."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию на поле."""
        self.position = (
            random.randrange(0, SCREEN_WIDTH, GRID_SIZE),
            random.randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        )

    def draw(self, surface):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку в центре экрана."""
        super().__init__()
        self.body_color = (0, 255, 0)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None  # Для затирания хвоста

    def get_head_position(self):
        """Возвращает координаты головы."""
        return self.positions[0]

    def update_direction(self):
        """Применяет новое направление."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну клетку."""
        head = self.get_head_position()
        x, y = self.direction

        # Прохождение сквозь стены (остаток от деления)
        new_x = (head[0] + x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head[1] + y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.__init__()

    def draw(self, surface):
        """Отрисовывает змейку и затирает её след."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

        # Затираем хвост, если змейка сдвинулась
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.display.set_caption('Изгиб Питона')

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Яблоко не должно появляться внутри змейки
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
